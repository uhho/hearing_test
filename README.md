# Hearing test

Simple hearing test

## Running

```sh
docker build -t hearing-test .
```

```sh
docker run --rm -it -v `pwd`:/workspace --device /dev/snd hearing-test python3 start.py
```

## Troubleshooting

Try to restart sound controller on your host machine

```sh
sudo alsa force-reload
```
