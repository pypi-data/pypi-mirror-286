from collections import defaultdict
import csv
import json
import logging
import math
from pathlib import Path
import re
from typing import Union, Optional, Literal, List, Tuple, Dict, Any
import urllib.parse
import re

from genson import SchemaBuilder
from mcap.writer import Writer
from roboto.domain import topics
from roboto_ingestion_utils.ingestion_utils import compute_checksum

from .metrics import RunningStats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


TYPE_MAPPING = {
        "string": str,
        "boolean": bool,
        "integer": int,
        "number": float,
        }

TYPE_MAPPING_CANONICAL = {
        "string": topics.CanonicalDataType.String,
        "boolean": topics.CanonicalDataType.Boolean,
        "number":  topics.CanonicalDataType.Number,
        "integer": topics.CanonicalDataType.Number
        }

MAX_UINT64 = 2**64 - 1


def sanitize_filename(user_string):
    unsafe_chars = re.compile(r'[<>:"/\\|?*\0]')

    sanitized = unsafe_chars.sub('_', user_string)

    safe_filename = urllib.parse.quote(sanitized, safe='')

    max_length = 255  # typical maximum length for filenames in Unix
    if len(safe_filename) > max_length:
        safe_filename = safe_filename[:max_length]

    return safe_filename


def create_json_schema(
        field_type_dict: Dict[str, str]
) -> Dict[str, Any]:
    """
    Creates a JSON schema based on a message definition.

    This function iterates over each field in the message definition and constructs
    a JSON schema. Fields starting with '_padding' are ignored. The function supports
    handling both array and non-array types.

    Args:
    - message_definition: A list of tuples, each representing a field in the message.
      Each tuple contains the field type, array size, and field name.

    Returns:
    - A dictionary representing the constructed JSON schema.
    """
    schema = {"type": "object", "properties": {}, "required": []}
    for field_name, field_type in field_type_dict.items():
        schema_property = {"type": field_type}

        schema["properties"][field_name] = schema_property
        schema["required"].append(field_name)

    return schema


def convert_value(field_type: str, value: Any) -> Any:
    """
    Converts a field value to its corresponding JSON type.

    Args:
    - field_type: The type of the field as a string.
    - value: The value to be converted.

    Returns:
    - The converted value in its appropriate JSON type, or None if conversion fails.
    """
    try:
        if field_type == "integer":
            value = int(value)
        elif field_type == "number":
            value = float(value)
        elif field_type == "boolean":
            value = bool(int(value))
        elif field_type == "json":
            value = json.loads(value)
        elif field_type == "string":
            value = str(value)
    except (ValueError, TypeError, json.JSONDecodeError) as e:
        print(f"Error converting value '{value}' to type '{field_type}': {e}")
        return None

    if field_type in ["integer", "number"]:
        if math.isnan(value) or math.isinf(value):
            print(f"Value '{value}' is NaN or Infinity, setting to None")
            return None

    return value


def infer_types(csv_line): 
    """
    infer type string from the first value in each csv
    """
    types = []
    for value in csv_line:
        if value.isnumeric(): # only 0-9, no ., etc
            types.append("number")
        elif re.match(r'^\d+\.\d+$', value):  # matches simple decimal numbers
            types.append("number")
        elif re.match(r'^[+-]?\d*\.?\d+([eE][+-]?\d+)?$', value):  # matches scientific notation
            types.append("number")
        elif value.lower() in ["true", "false"]:
            types.append("boolean")
        # try to parse as json
        elif value[0] == "{" and value[-1] == "}":
            try:
                json.loads(value)
                types.append("json")
            except:
                types.append("string")
        else:
            types.append("string")
    return types


def format_field_name(orig_name: str):
    """
    replace whitespace, periods, and slashes
    """
    orig_name = orig_name.strip()
    disallowed_chars = "./\\ "
    for char in disallowed_chars:
        orig_name = orig_name.replace(char, "_")
    return orig_name


def infer_timestamp_column(fields: List):
    column_idx = None
    # TODO @YVES: pick better priorities/list of smart guesses
    candidate_stubs = ['timestamp', 'timestamp [ms]', 'timestamp [µs]', 'time', 'offset', 'ts', 'seconds']
    for candidate in candidate_stubs:
        if not column_idx:
            for idx, field_name in enumerate(fields):
                if not column_idx:
                    if candidate in field_name.lower():
                        column_idx = idx
                        logger.info(f"Found probable timestamp key `{field_name}`")
                        break
                else:
                    break
        else:
            break
    if column_idx:
        return column_idx
    else:
        return 0    # default to returning the first column if you can't find anything


def resolve_paths(input_dir: Union[str, Path], rel_file_path: Union[str, Path], output_dir: Union[str, Path]) -> Tuple[Path, Path, Path]:
    """Resolve and return Path objects for input and output directories and CSV file."""
    if isinstance(input_dir, str):
        input_dir = Path(input_dir)
    if isinstance(output_dir, str):
        output_dir = Path(output_dir)
    csv_file = input_dir / rel_file_path
    if isinstance(csv_file, str):
        csv_file = Path(csv_file).resolve()
    return input_dir, output_dir, csv_file


def initialize_variables() -> Tuple[List[str], Dict[str, List[Tuple[int, Tuple[str, str]]]], Dict[str, str], Dict[str, SchemaBuilder], Optional[int]]:
    """Initialize and return variables needed for processing."""
    field_names = []
    raw_msg_lists = {}
    field_type_mappings = {}
    json_field_schemes = {}
    timestamp_column = None
    return field_names, raw_msg_lists, field_type_mappings, json_field_schemes, timestamp_column


def infer_timestamp_column_from_header(field_names: List[str]) -> int:
    """Infer the timestamp column from the header if not provided."""
    if 'timestamp' in field_names:
        return field_names.index('timestamp')
    else:
        logger.info("Inferring timestamp from available keys...")
        return infer_timestamp_column(field_names)


def process_header(header: List[str],
                   timestamp_key: Optional[str],
                   csv_file: str) -> Tuple[List[str], int]:
    """Process the header row of the CSV file."""
    field_names = [format_field_name(str(x)) for x in header]
    timestamp_key = format_field_name(timestamp_key)
    if timestamp_key:
        if timestamp_key not in field_names:
            logger.warning(f"Error: {timestamp_key} must be a valid key in file {csv_file}: {field_names}")
            timestamp_column = infer_timestamp_column_from_header(field_names)
            logger.warning(f"Inferring timestamp column as {field_names[timestamp_column]}")
        else:
            timestamp_column = field_names.index(timestamp_key)
    else:
        timestamp_column = infer_timestamp_column_from_header(field_names)
    field_names.pop(timestamp_column)
    return field_names, timestamp_column


def process_line(line: List[str],
                 timestamp_column: int) -> Tuple[str, List[str]]:
    """Process a single line of the CSV file."""
    timestamp_raw = line.pop(timestamp_column)
    return timestamp_raw, line


def infer_field_types(line: List[str],
                      field_names: List[str]) -> Tuple[Dict[str, str], Dict[str, SchemaBuilder]]:
    """Infer the types of the fields in the CSV file."""
    field_types = infer_types(line)
    field_type_mappings = {name: type_str for name, type_str in zip(field_names, field_types)}
    json_field_schemes = {name: SchemaBuilder() for name in field_names if field_type_mappings[name] == "json"}
    return field_type_mappings, json_field_schemes


def convert_timestamp(timestamp_raw: str, timestamp_format: Literal["seconds", "milliseconds", "nanoseconds"]) -> int:
    """Convert the timestamp to nanoseconds."""
    timestamp = float(timestamp_raw)
    if timestamp_format == "seconds":
        timestamp *= 1e9
    elif timestamp_format == "milliseconds":
        timestamp *= 1e6
    elif timestamp_format == "microseconds":
        timestamp *= 1e3
    return int(timestamp)


def collect_message_stats(raw_msg_list: List[Tuple[int, Tuple[str, str]]]) -> Tuple[int, int, int]:
    """Collect statistics about the messages."""
    msg_count = len(raw_msg_list)
    start_time_ns = raw_msg_list[0][0]
    end_time_ns = raw_msg_list[-1][0]
    return msg_count, start_time_ns, end_time_ns


def prepare_output_file(csv_file: Path, field: str, output_dir: Path) -> Path:
    """Prepare the output file for writing the MCAP data."""
    topic_fname = f"{csv_file.stem}_{field}.mcap"
    logger.info(f"Preparing file: {topic_fname}")
    topic_mcap_file = output_dir / topic_fname
    topic_mcap_file.parent.mkdir(parents=True, exist_ok=True)
    return topic_mcap_file


def remove_null_characters(file_path):
    """Remove null characters from the file."""
    with open(file_path, 'rb') as f:
        content = f.read().replace(b'\x00', b'')
    with open(file_path, 'wb') as f:
        f.write(content)


def csv_to_mcap(
        input_dir: Union[str, Path],
        rel_file_path: Union[str, Path],
        output_dir: Union[str, Path],
        calculate_metrics: bool = True,
        timestamp_key: Optional[str] = None,
        timestamp_format: Literal["seconds", "milliseconds", "nanoseconds"] = "nanoseconds"
):
    """
    Ingest one csv and save an MCAP file for each column
    to the output directory output_dir. Optionally calculate metrics
    """

    input_dir, output_dir, csv_file = resolve_paths(input_dir, rel_file_path, output_dir)

    field_names, _, field_type_mappings, json_field_schemes, timestamp_column = initialize_variables()

    topic_stats = defaultdict(RunningStats)
    topic_mcap_files = {}
    json_schema_topic = {}
    schema_checksums = {}
    writers = {}  # Dictionary to store writers for each field

    remove_null_characters(csv_file)

    with open(csv_file, 'r') as f:
        # Read the lines from the file
        lines = f.readlines()

    if not lines:
        print(f"Error: Empty file: {csv_file}")
        return {}, {}, {}, {}

    # Remove trailing comma from each line
    cleaned_lines = [line.strip() for line in lines]
    cleaned_lines = [line.rstrip(',\n') + '\n' for line in cleaned_lines]

    reader = csv.reader(cleaned_lines)
    field_names, timestamp_column = process_header(next(reader), timestamp_key, csv_file.name)
    field_type_mappings, json_field_schemes = None, None
    start_time_ns = None
    end_time_ns = None
    for i, line in enumerate(reader):
        timestamp_raw, line = process_line(line, timestamp_column)
        timestamp = convert_timestamp(timestamp_raw, timestamp_format)

        if start_time_ns is None:
            start_time_ns = timestamp

        end_time_ns = timestamp
        line = [entry.strip() for entry in line]

        if i == 0:
            field_type_mappings, json_field_schemes = infer_field_types(line, field_names)
            for field in field_names:
                file_name = sanitize_filename(f"{csv_file.stem}_{field}.mcap")
                topic_mcap_file = output_dir / file_name
                topic_mcap_files[field] = str(topic_mcap_file)

                stream = open(topic_mcap_file, "wb")
                writer = Writer(stream)
                writer.start()
                json_schema_topic_per_field = create_json_schema(
                    field_type_dict={field: field_type_mappings[field]})
                schema_id = writer.register_schema(
                    name=f"{csv_file.stem}",
                    encoding="jsonschema",
                    data=json.dumps(json_schema_topic_per_field).encode(),
                )
                channel_id = writer.register_channel(
                    schema_id=schema_id,
                    topic=f"{csv_file.stem}",
                    message_encoding="json",
                )
                schema_checksums[field] = compute_checksum(json_schema_topic_per_field)

                writers[field] = (writer, stream, channel_id)

        for j, val in enumerate(line):
            field = field_names[j]
            field_type = field_type_mappings[field]
            if field_type == "json":
                json_field_schemes[field].add_object(val)
            raw_msg = (field_type, val)
            json_msg_instance = {field: convert_value(raw_msg[0], raw_msg[1])}

            writer, stream, channel_id = writers[field]
            writer.add_message(
                channel_id=channel_id,
                log_time=timestamp,
                sequence=i,
                data=json.dumps(json_msg_instance).encode("utf-8"),
                publish_time=timestamp,
            )

            if calculate_metrics:
                for path, value in json_msg_instance.items():
                    if isinstance(value, (int, float)):
                        topic_stats[path].update(value)

    # Close all writers
    for writer, stream, _ in writers.values():
        writer.finish()
        stream.close()

    topic_metrics_dict = {}
    if calculate_metrics:
        for path, stats in topic_stats.items():
            topic_metrics_dict[path] = stats.get_stats()

    print(topic_metrics_dict)

    topic_name = csv_file.stem
    msg_count = i + 1  # i starts from 0

    topic_info_entry = {
        "topic_name": topic_name,
        "mcap_path": topic_mcap_files,
        "nr_msgs": msg_count,
        "first_timestamp": start_time_ns,
        "last_timestamp": end_time_ns,
        "msg_type": json_schema_topic,
        "checksum": schema_checksums
    }

    topic_info_dict = {topic_name: topic_info_entry}

    return topic_info_dict, topic_metrics_dict, {}, field_type_mappings


def create_message_path_records(field_type_dict: dict, metrics_dict: dict) -> List:
    """
    Creates message path records for a given topic.

    Args:
    - topic: The topic object to which the message paths will be added.
    - field_data: A list of field data objects containing the message definition.
    """
    message_path_list = list()

    for field_name, field_type in field_type_dict.items():
        if field_type not in TYPE_MAPPING_CANONICAL.keys():
            canonical_data_type = topics.CanonicalDataType.Unknown
        else:
            canonical_data_type = TYPE_MAPPING_CANONICAL[field_type]
        
        metadata_dict = dict()
        if field_name in metrics_dict.keys():
            metadata_dict = metrics_dict[field_name]

        message_path_list.append(topics.AddMessagePathRequest(
                message_path=field_name,
                data_type=field_type,
                canonical_data_type=canonical_data_type,
                metadata=metadata_dict,
            )
        )

        logger.info(
            f"Adding field: {field_name}, type: {field_type}, canonical: {canonical_data_type}"
        )
    return message_path_list
