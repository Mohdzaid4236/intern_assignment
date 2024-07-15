import re

def parse_ass_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    headers = []
    events = []
    is_event_section = False

    for line in lines:
        if line.startswith('[Events]'):
            is_event_section = True
            headers.append(line)
        elif is_event_section:
            if line.startswith('Dialogue:'):
                events.append(line)
            else:
                headers.append(line)
        else:
            headers.append(line)

    return headers, events

def modify_events(events):
    modified_events = []
    for i, event in enumerate(events):
        previous_event = events[i-1] if i > 0 else 'Dialogue: 0,0:00:00.00,0:00:00.00,...'
        next_event = events[i+1] if i < len(events) - 1 else 'Dialogue: 0,0:00:00.00,0:00:00.00,...'

        # Extract text of previous, current, and next events
        previous_text = re.search(r'Dialogue: \d+,\d+:\d+:\d+\.\d+,\d+:\d+:\d+\.\d+,.*?,.*,.*,.*,.*,.*?,(.*)', previous_event).group(1)
        current_text = re.search(r'Dialogue: \d+,\d+:\d+:\d+\.\d+,\d+:\d+:\d+\.\d+,.*?,.*,.*,.*,.*,.*?,(.*)', event).group(1)
        next_text = re.search(r'Dialogue: \d+,\d+:\d+:\d+\.\d+,\d+:\d+:\d+\.\d+,.*?,.*,.*,.*,.*,.*?,(.*)', next_event).group(1)

        modified_text = f"{previous_text} {current_text} {next_text}"
        modified_event = re.sub(r'(Dialogue: \d+,\d+:\d+:\d+\.\d+,\d+:\d+:\d+\.\d+,.*?,.*,.*,.*,.*,.*?,).*', r'\1' + modified_text, event)
        
        modified_events.append(modified_event)

    return modified_events

def write_output_file(file_path, headers, events):
    with open(file_path, 'w', encoding='utf-8') as file:
        for header in headers:
            file.write(header)
        for event in events:
            file.write(event)

if __name__ == "__main__":
    input_file = 'input.ass'
    output_file = 'output.ass'

    headers, events = parse_ass_file(input_file)
    modified_events = modify_events(events)
    write_output_file(output_file, headers, modified_events)
