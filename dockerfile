FROM python:3.9

# 
WORKDIR /lms-python-chile

# 
COPY ./ /lms-python-chile/

# 
RUN pip install --no-cache-dir --upgrade -r /lms-python-chile/requirements.txt

COPY ./ /lms-python-chile/

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]