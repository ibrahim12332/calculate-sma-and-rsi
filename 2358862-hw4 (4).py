import csv

#  you have to load the data from the orcl.csv file into  list of dictionaries
def load_data(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

data = load_data('orcl.csv')

# To calculate the SMA for each 5 days of the data
def calculate_sma(data, window=5):
    sma_values = []
    # for loop to each day of the data
    for i in range(len(data)):
        # strat calculating after day 4 
        if i >= window - 1:
            # a list of the values if each day of the last five days
            window_prices = [float(data[j]['Close']) for j in range(i - window + 1, i + 1)]
            # sum the values and devide them by 5
            sma = sum(window_prices) / window
            # Add them to the sma list
            sma_values.append({'Date': data[i]['Date'], 'SMA': sma})
    return sma_values

sma_data = calculate_sma(data)

# Function to calculate the RSI on 14 days period
def calculate_rsi(data, periods=14):
    # initial our lists
    gain = []
    losse = []
    rsi_values = []

    
    for i in range(1, len(data)):
        # Calculate the change in Close price by each day 
        change = float(data[i]['Close']) - float(data[i - 1]['Close'])
        # if the change is in positive that means add it to the gain list otherwise add 0
        gain.append(max(change, 0))
        # if the change is in negative that means add it to the losse list otherwise add 0
        losse.append(abs(min(change, 0)))

        # start after the period day which is 14
        if i >= periods:
            # start calculating avrage in the gain and loss for each day deviding it by the period
            avg_gain = sum(gain[-periods:]) / periods
            avg_loss = sum(losse[-periods:]) / periods
            # the folrmula you gave in the pdf
            rs = avg_gain / avg_loss if avg_loss != 0 else 0
            rsi = 100 - (100 / (1 + rs))
            rsi_values.append({'Date': data[i]['Date'], 'RSI': rsi})

    return rsi_values

rsi_data = calculate_rsi(data)


# a function for creating the csv files
def write_to_csv(data, filename):
    # w its for writing
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

write_to_csv(sma_data, 'orcl-sma.csv')
write_to_csv(rsi_data, 'orcl-rsi.csv')
