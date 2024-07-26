from PIL import Image
from pathlib import Path
import time
from typing import List, Literal, Optional, Union
from datetime import datetime
from mcap_protobuf.writer import Writer
from foxglove_schemas_protobuf.CompressedImage_pb2 import CompressedImage
from io import BytesIO

import re

from roboto.domain import topics
from roboto_ingestion_utils import ingestion_utils


ALLOWED_IMG_FORMATS = ["png", "jpg", "jpeg"]

def create_image_message_path_request(message_path_name: str):
    message_path = topics.AddMessagePathRequest(
            message_path=message_path_name,
            data_type="image",
            canonical_data_type=topics.CanonicalDataType.Image,
            )
    return [message_path]

def image_to_message(fname: Union[str, Path], 
                     timestamp: int, 
                     timestamp_format: str):
    if isinstance(fname, str):
        fname = Path(fname)

    ext = fname.suffix.lower()[1:] # remove period from extension
    assert ext in ALLOWED_IMG_FORMATS, f"Error: expected an image format from {ALLOWED_IMG_FORMATS}, received {ext}"
    msg = CompressedImage()
    if timestamp_format == "seconds":
        msg.timestamp.FromSeconds(timestamp)
    elif timestamp_format == "milliseconds":
        msg.timestamp.FromMilliseconds(timestamp)
    elif timestamp_format == "microseconds":
        msg.timestamp.FromMicroseconds(timestamp)
    elif timestamp_format == "nanoseconds":
        msg.timestamp.FromNanoseconds(timestamp)
    else:
        raise ValueError(f"Error: timestamp must be in format seconds, milliseconds, microseconds, or nanoseconds, received {timestamp_format}")
    raw_img = Image.open(fname)
    buffer = BytesIO()
    # convert jpg to jpeg
    raw_img.save(buffer, format='jpeg')
    msg.data = buffer.getvalue()
    msg.format = 'JPEG' 
    return msg

def image_dir_to_mcap(input_dir: Path,
                      timestamp_format: str="nanoseconds",
                      img_format: Optional[str]=None,
                      start_timestamp: Optional[int]=None,
                      frame_rate: Optional[int]=None,
                      timestamps: Optional[List]=None,
                      ):
    """
    Ingest a directory of images to an mcap file
    using the CompressedImage protobuf format
    """
    if img_format:
        assert img_format.lower() in ALLOWED_IMG_FORMATS, f"Error: expected one of {ALLOWED_IMG_FORMATS}, received {img_format}"
    
    assert (frame_rate is not None and start_timestamp is not None) or timestamps is not None, "Error: must provide one of a timestamp list or a framerate at which to create timestamps"
    assert timestamp_format, "timestamp must be passed with a timestamp format string."

    # create a list of all image files of specified format in the input dir
    if img_format:
        image_files = [x for x in input_dir.glob(f"*{img_format}")]
    else:
        image_files = []
        for fmt in ALLOWED_IMG_FORMATS + [x.upper() for x in ALLOWED_IMG_FORMATS]:

            image_files.extend([x for x in input_dir.glob(f"*.{fmt}")])
    
    assert image_files, f"Error: no image files in {input_dir}"

    # Sort image files using custom logic
    sorted_img_files = sorted(image_files, key=custom_sort_key)


    rel_file_path = image_files[0] 

    # setup temp output directory
    output_dir_topic, output_dir_temp = ingestion_utils.setup_output_folder_structure(
            input_dir=str(input_dir),
            file_path=str(input_dir / rel_file_path)
            )
    output_dir_topic = Path(output_dir_topic)

    if frame_rate is not None and start_timestamp is not None:
        timestamps = [start_timestamp + int(x/frame_rate * 1e9) for x in range(len(sorted_img_files))]

    assert len(timestamps) == len(image_files), "Error: each image must have one timestamp,\
                            received {len(image_files) images and len(timestamps) timestamps}"

    # Write out to MCAP
    topic_name = input_dir.stem 
    fname = str(output_dir_topic / f"{topic_name}.mcap")
    with open(fname, "wb") as f:
        writer = Writer(f)
        for timestamp, image in zip(timestamps, sorted_img_files):
            image_msg = image_to_message(image,
                                         timestamp=timestamp,
                                         timestamp_format=timestamp_format)
            writer.write_message(
                topic=topic_name,
                message=image_msg,
                    )
        writer.finish()

    topic_entry = {}

    topic_entry["first_timestamp"] = timestamps[0] 
    topic_entry["last_timestamp"] = timestamps[-1]
    topic_entry["nr_msgs"] = len(sorted_img_files)
    topic_entry["mcap_path"] = fname
    topic_info_dict = {topic_name: topic_entry}

    return topic_info_dict, None, {}, {}

# custom sorting logic: extract number from file_name
# and use as sorting key, irrespective of zero-padding
def extract_number(file_path):
    file_name = file_path.name
    match = re.search(r'(\d+)', file_name)
    return int(match.group(0)) if match else None

def custom_sort_key(file_name):
    number_part = extract_number(file_name)
    if number_part is not None:
        return (0, number_part)
    else:
        return (1, file_name)
        
