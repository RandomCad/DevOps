FROM rust:1.80-alpine AS builder

RUN apk add --no-cache libc-dev

WORKDIR /chamaeleon
RUN cargo new chamaeleon
WORKDIR /chamaeleon
COPY Cargo.toml Cargo.lock ./
RUN cargo build --release

COPY src ./src
RUN touch src/main.rs; \
    cargo build --release

FROM alpine AS runtime

WORKDIR /app

COPY --from=builder /chamaeleon/target/release/chamaeleon ./

ENV ROCKET_ADDRESS="0.0.0.0"

EXPOSE 8000

CMD ["./chamaeleon"]
