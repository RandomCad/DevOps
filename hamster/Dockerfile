FROM rust:1.80-alpine AS builder

RUN apk add --no-cache libc-dev

WORKDIR /
COPY Cargo.toml Cargo.lock /
RUN sed -i "s|members = .*|members = []|g" Cargo.toml; \
    cargo new hamster
WORKDIR /hamster
COPY hamster/Cargo.toml ./
RUN cargo build --release

COPY hamster/src ./src
RUN touch src/main.rs; \
    cargo build --release

FROM alpine AS runtime

WORKDIR /app

RUN mkdir files

COPY --from=builder /target/release/hamster ./

ENV ROCKET_ADDRESS="0.0.0.0"

EXPOSE 8000

CMD ["./hamster"]
