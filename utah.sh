
# Run proration, but only get the report.
# echo "Starting preprocessing to generate a report."
# python3 /Users/apizzimenti/desktop/Preprocessing/main.py
# mv /Users/apizzimenti/desktop/Preprocessing/Proration.html $(pwd)/output/Proration.html

# Run the data analysis (to make sure it's all updated)
echo "Running data analysis on the dual graph."
python3 analysis.py

# Then, run the chain and save the output to the info directory.
echo "Running chain."
python3 chain.py $1