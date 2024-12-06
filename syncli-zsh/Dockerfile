# Use Python 3.10 as the base image
FROM python:3.10-slim

# Set environment variables
ENV SHELL=/bin/zsh
ENV HISTFILE=/root/.zsh_history
ENV HISTSIZE=1000
ENV SAVEHIST=1000

# Set the working directory
WORKDIR /app

# Install system dependencies including full shell utilities
RUN apt-get update && apt-get install -y \
    bash \
    zsh \
    zsh-common \
    bash-completion \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up Zsh and configure history
RUN chsh -s /bin/zsh && \
    echo "setopt INC_APPEND_HISTORY" >> /root/.zshrc && \
    echo "setopt SHARE_HISTORY" >> /root/.zshrc && \
    echo "setopt EXTENDED_HISTORY" >> /root/.zshrc && \
    echo "SAVEHIST=1000" >> /root/.zshrc && \
    echo "HISTSIZE=1000" >> /root/.zshrc && \
    echo "HISTFILE=/root/.zsh_history" >> /root/.zshrc

# Create and set permissions for history files
RUN touch /root/.zsh_history /root/.bash_history \
    && chmod 600 /root/.zsh_history /root/.bash_history

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create history mount point
RUN mkdir -p /history

# Create entrypoint script
RUN echo '#!/bin/zsh\n\
if [ -f /history/.zsh_history ]; then\n\
    cp /history/.zsh_history $HISTFILE\n\
fi\n\
if [ -f /history/.bash_history ]; then\n\
    cp /history/.bash_history /root/.bash_history\n\
fi\n\
python main.py &\n\
exec zsh\n\
' > /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]