extern crate anyhow;
extern crate cpal;

mod wav;

use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};

fn main() -> Result<(), anyhow::Error> {
    let host = cpal::default_host();
    let device = host
        .default_output_device()
        .expect("failed to find a default output device");
    let config = device.default_output_config()?;

    match config.sample_format() {
        cpal::SampleFormat::F32 => run::<f32>(&device, &config.into())?,
        cpal::SampleFormat::I16 => run::<i16>(&device, &config.into())?,
        cpal::SampleFormat::U16 => run::<u16>(&device, &config.into())?,
    }

    std::thread::sleep(std::time::Duration::from_secs(5));

    Ok(())
}

fn run<T>(device: &cpal::Device, config: &cpal::StreamConfig) -> Result<(), anyhow::Error>
where
    T: cpal::Sample,
{
    let channels = config.channels as usize;

    let mut wav = wav::WavSlice::new("input/piano.wav");
    wav.apply_repeat(5);
    wav.apply_speed_change(0.25*10.0);
    let mut read_head = wav::ReadHead::new(wav.clone());

    let mut wav2 = wav::WavSlice::new("input/piano.wav");
    let mut read_head2 = wav::ReadHead::new(wav2.clone());

    let mut next_value =  move || {
        read_head.get_next() +
        read_head2.get_next() / 2 as i16
    };

    let err_fn = |err| eprintln!("an error occurred on stream: {}", err);

    let stream = device.build_output_stream(
        config,
        move |data: &mut [T], _: &cpal::OutputCallbackInfo| {
            //println!("test");
            write_data(data, channels, &mut next_value)
        },
        err_fn,
    )?;
    stream.play()?;

    std::thread::sleep(std::time::Duration::from_secs(10));

    Ok(())
}

fn write_data<T>(output: &mut [T], channels: usize, next_sample: &mut dyn FnMut() -> i16)
where
    T: cpal::Sample,
{
    for frame in output.chunks_mut(channels) {
        let value: T = cpal::Sample::from::<i16>(&next_sample());
        for sample in frame.iter_mut() {
            *sample = value;
        }
    }
}
