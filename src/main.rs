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

    //match config.sample_format() {
    //    cpal::SampleFormat::F32 => run::<f32>(&device, &config.into())?,
    //    cpal::SampleFormat::I16 => run::<i16>(&device, &config.into())?,
    //    cpal::SampleFormat::U16 => run::<u16>(&device, &config.into())?,
    //}

    run::<i16>(&device, &config.into());
    Ok(())
}

fn run<T>(device: &cpal::Device, config: &cpal::StreamConfig) -> Result<(), anyhow::Error>
where
    T: cpal::Sample,
{
    let sample_rate = config.sample_rate.0 as f32;
    let channels = config.channels as usize;

    let mut wav = wav::WavSlice::new("input/piano.wav");
    // Produce a sinusoid of maximum amplitude.
    //let mut sample_clock = 0f32;
    //let mut next_value = move || {
    //    sample_clock = (sample_clock + 1.0) % sample_rate;
    //    (sample_clock * 440.0 * 2.0 * 3.141592 / sample_rate).sin() * 0.2
    //};

    let mut next_value =  move || {
        match wav.slice_samples.iter().next() {
            Some(v) => { *v },
            None => { eprintln!("no sample found"); 0i16 }
        }
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

    std::thread::sleep(std::time::Duration::from_millis(10000));

    Ok(())
}

fn write_data<T>(output: &mut [T], channels: usize, next_sample: &mut dyn FnMut() -> i16)
where
    T: cpal::Sample,
{
    //println!("{:?}", channels);
    for frame in output.chunks_mut(channels) {
        let value: T = cpal::Sample::from::<i16>(&next_sample());
        for sample in frame.iter_mut() {
            *sample = value;
        }
    }
}
