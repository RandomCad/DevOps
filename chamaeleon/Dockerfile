FROM rust:1.80-alpine AS builder

RUN apk add --no-cache libc-dev

WORKDIR /
COPY Cargo.toml Cargo.lock /
RUN sed -i "s|members = \\[[^\\]]*\\]|members = \\[\\]|g" Cargo.toml; \
    cargo new chamaeleon
WORKDIR /chamaeleon
COPY chamaeleon/Cargo.toml ./
RUN cargo build --release

COPY chamaeleon/src ./src
RUN touch src/main.rs; \
    cargo build --release

FROM alpine AS runtime

WORKDIR /app

COPY --from=builder /target/release/chamaeleon ./

ENV ROCKET_ADDRESS="0.0.0.0"

EXPOSE 8000

CMD ["./chamaeleon"]
