FROM python:3.8-slim

LABEL maintainer=branislav.bajuzik@gmail.com

WORKDIR /pdf

# Get libs
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       poppler-utils && \
    # Cleanup
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Install Python Dependencies
COPY requirements.txt ./

RUN python -m pip install -r requirements.txt && \
    # Cleanup
    rm -rf /root/.cache

# Copy code
COPY pdf_server/ pdf_server/
COPY pdf_worker/ pdf_worker/
COPY docker/config.json pdf_server/config.json
