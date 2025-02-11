# Use lightweight Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy files
COPY manga_recommender.py my_dataset.csv requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the script when the container starts
CMD ["python", "manga_recommender.py"]

