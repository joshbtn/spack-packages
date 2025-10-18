FROM debian:bookworm AS base

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    python3 \
    python3-pip \
    vim \
    wget \
    && rm -rf /var/lib/apt/lists/*

FROM base AS devcontainer

RUN git clone --depth=2 --branch=releases/v1.0 https://github.com/spack/spack.git ~/spack
    echo "source ~/spack/share/spack/setup-env.sh" >> ~/.bashrc