NUMBER_OF_MEASUREMENTS = 11
NUMBER_OF_METRICS = 3
NUMBER_OF_LINES_PER_RECORD = 20


def read_measurement_file(filename):
    number_of_records = 0
    current_line = 0
    measurement_x = []
    metric_x = []
    measurement_y = []
    metric_y = []
    colours = []
    measurement_labels = []
    metric_labels = []
    current_record = []
    previous_record = []
    try:
        # Open the measurement file in read only
        file = open(filename, "r")
        # Read all of the lines from the file for ease of processing
        lines = file.readlines()
        # Loop over all of the lines
        for line in lines:
            # Current line we are processing in the data
            current_line += 1
            # Records are separated by a line of hyphens
            if '—————————' in line:
                number_of_records += 1

                # The colours we are going to plot each body part as, the index of this array directly aligns with the index of the labels
                colours += '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#5cb377'
                measurement_labels += 'Neck', 'Shoulders', 'Resting bicep', 'Tensed bicep', 'Forearm', 'Wrist', 'Chest', 'Waist', 'Hips', 'Quad', 'Calf'
                metric_labels += 'Body weight (kg)', 'Body fat (%)', 'WHR'

                # Save the current record as the previous now we are finished processing it
                previous_record = current_record

                # Read entire record from the file, containing all measurements and metrics
                current_record = lines[current_line:current_line + NUMBER_OF_LINES_PER_RECORD]

                # Isolate the date for this current record
                date = current_record[1].split('-')[0].strip()

                # Iterate over all of the measurements
                for i in range(3, 3 + NUMBER_OF_MEASUREMENTS, 1):
                    measurement_x += [date]
                    if 'bicep' in current_record[i]:
                        measurement_y += [current_record[i].split(' ')[2].strip('”')]
                    else:
                        measurement_y += [current_record[i].split(' ')[1].strip('”')]

                # Iterate over all of the metrics
                for i in range(15, 15 + NUMBER_OF_METRICS, 1):
                    if 'Body weight' in current_record[i]:
                        metric_x += [date]
                        metric_y += [current_record[i].split(' ')[2].strip('kg\n')]
                    elif 'Body fat' in current_record[i]:
                        metric_x += [date]
                        metric_y += [current_record[i].split(' ')[2].strip('%')]
                    elif 'WHR' in current_record[i]:
                        metric_x += [date]
                        metric_y += [current_record[i].split(' ')[4]]
            else:
                continue

        # Iterate over all of the measurements
        for i in range(3, 3 + NUMBER_OF_MEASUREMENTS, 1):
            # Calculate the trend
            if len(previous_record) > 0:
                if 'bicep' in current_record[i]:
                    # Get the current and the previous measurement for this body part
                    current_measurement_y = [current_record[i].split(' ')[2].strip('”')]
                    previous_measurement_y = [previous_record[i].split(' ')[2].strip('”')]
                else:
                    # Get the current and the previous measurement for this body part
                    current_measurement_y = [current_record[i].split(' ')[1].strip('”')]
                    previous_measurement_y = [previous_record[i].split(' ')[1].strip('”')]

                # If it has increased, add a + to the end of the label
                if current_measurement_y > previous_measurement_y:
                    if '+' in measurement_labels[i - 3]:
                        continue
                    elif '-' in measurement_labels[i - 3]:
                        measurement_labels[i - 3] = measurement_labels[i - 3][:-1] + '+'
                    else:
                        measurement_labels[i - 3] += ' +'
                # If it has decreased add a -
                elif current_measurement_y < previous_measurement_y:
                    if '-' in measurement_labels[i - 3]:
                        continue
                    elif '+' in measurement_labels[i - 3]:
                        measurement_labels[i - 3] = measurement_labels[i - 3][:-1] + '-'
                    else:
                        measurement_labels[i - 3] += ' -'
                # No change at all then add nothing, but remove any existing monikers
                else:
                    if '-' in measurement_labels[i - 3] or '+' in measurement_labels[i - 3]:
                        measurement_labels[i - 3] = measurement_labels[i - 3][:-1]

        # Iterate over all of the metrics
        for i in range(15, 15 + NUMBER_OF_METRICS, 1):
            # Calculate the trend
            if len(previous_record) > 0:
                if 'Body weight' in current_record[i]:
                    # Get the current and the previous measurement for this body part
                    current_metric_y = [current_record[i].split(' ')[2].strip('kg\n')]
                    previous_metric_y = [previous_record[i].split(' ')[2].strip('kg\n')]
                elif 'Body fat' in current_record[i]:
                    # Get the current and the previous measurement for this body part
                    current_metric_y = [current_record[i].split(' ')[2].strip('%')]
                    previous_metric_y = [previous_record[i].split(' ')[2].strip('%')]
                elif 'WHR' in current_record[i]:
                    # Get the current and the previous measurement for this body part
                    current_metric_y = [current_record[i].split(' ')[4]]
                    previous_metric_y = [previous_record[i].split(' ')[4]]
                else:
                    continue

                # If it has increased, add a + to the end of the label
                if current_metric_y > previous_metric_y:
                    if '+' in metric_labels[i - 15]:
                        continue
                    elif '-' in metric_labels[i - 15]:
                        metric_labels[i - 15] = metric_labels[i - 15][:-1] + '+'
                    else:
                        metric_labels[i - 15] += ' +'
                # If it has decreased add a -
                elif current_metric_y < previous_metric_y:
                    if '-' in metric_labels[i - 15]:
                        continue
                    elif '+' in metric_labels[i - 15]:
                        metric_labels[i - 15] = metric_labels[i - 15][:-1] + '-'
                    else:
                        metric_labels[i - 15] += ' -'
                # No change at all then add nothing, but remove any existing monikers
                else:
                    if '-' in metric_labels[i - 15] or '+' in metric_labels[i - 15]:
                        metric_labels[i - 15] = metric_labels[i - 15][:-1]

        return measurement_x, measurement_y, metric_x, metric_y, colours, measurement_labels, metric_labels
    except Exception as e:
        print(e)
