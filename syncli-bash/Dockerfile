# Use Python 3.10 as the base image
FROM python:3.10-slim

# Set environment variables
ENV SHELL=/bin/bash
ENV HISTFILE=/root/.bash_history
ENV HISTSIZE=1000
ENV HISTFILESIZE=2000
ENV HISTTIMEFORMAT="%F %T "

# Set the working directory
WORKDIR /app

# Install system dependencies including full shell utilities
RUN apt-get update && apt-get install -y \
    bash \
    bash-completion \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configure bash history
RUN echo "export HISTFILE=/root/.bash_history" >> /root/.bashrc && \
    echo "export HISTSIZE=1000" >> /root/.bashrc && \
    echo "export HISTFILESIZE=2000" >> /root/.bashrc && \
    echo "export HISTTIMEFORMAT='%F %T '" >> /root/.bashrc && \
    echo "shopt -s histappend" >> /root/.bashrc && \
    echo "PROMPT_COMMAND='history -a; history -c; history -r'" >> /root/.bashrc && \
    echo "source /etc/bash_completion" >> /root/.bashrc

# Create and set permissions for history file
RUN touch /root/.bash_history \
    && chmod 600 /root/.bash_history \
    && chown root:root /root/.bash_history

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create history mount point
RUN mkdir -p /history

# Create entrypoint script with history initialization
RUN echo '#!/bin/bash\n\
if [ -f /history/.bash_history ]; then\n\
    cp /history/.bash_history $HISTFILE\n\
fi\n\
source /root/.bashrc\n\
history -r\n\
python main.py &\n\
exec bash --login\n\
' > /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]