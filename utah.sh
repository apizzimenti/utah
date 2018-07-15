
# Check to see that Preprocessing is installed. if so, then we run proration
# and get the report + protated data.
if [ -d ./Preprocessing ]
   then
        echo "Starting preprocessing to generate a report."
        python3 ./Preprocessing/main.py
        mv ./Prorated.* ./Prorated/
        mv ./Proration.html ./output/Proration.html
        mv ./Proration_images ./output/Proration_images
    else
        echo "Preprocessing library not installed - skipping."
fi

# Run the data analysis (to make sure it's all updated)
echo "Running data analysis on the dual graph."
python3 analysis.py

# Then, run the chain and save the output to the info directory.
echo "Running chain."
python3 chain.py $1