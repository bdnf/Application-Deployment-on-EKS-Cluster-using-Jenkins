FROM python:3.7.3-stretch

## Step 1:
# Create a working directory
WORKDIR /app
COPY requirements.txt /app

## Step 2:
# Install packages from requirements.txt
# hadolint ignore=DL3013
RUN pip3 --no-cache-dir install -r requirements.txt

## Step 3:
# Copy source code to working directory
COPY . /app

## Step 4:
# Expose port 80
EXPOSE 80

## Step 5:
# Run app.py at container launch
CMD ["python3", "app.py"]
