FROM public.ecr.aws/lambda/python:3.12

# Install Rust
RUN microdnf install -y rust

# Install Rustup
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Add Cargo to the PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Verify installation
RUN cargo --version

# Update pip
RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel -v

RUN pip list

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install --use-pep517 -r requirements.txt

# Create directory for function code
# WORKDIR ${LAMBDA_TASK_ROOT}/embed_docs_handler

# Copy function code to the embed_docs_handler directory
COPY ./embed_docs_handler/embed_docs_handler.py .
COPY ./embed_docs_handler/__init__.py .
COPY ./embed_docs_handler/embedding .

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
# CMD ["embed_docs_handler.handle_embed_docs"]
CMD ["embed_docs_handler.lambda_handler"]