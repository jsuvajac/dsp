use hound;
use std::path::Path;

#[derive(Debug)]
struct WavSlice {
    samples: Vec<i16>,
    slice_samples: Vec<i16>,
    len: usize
}

impl WavSlice {
    fn new(path: &'static str) -> WavSlice {
        let mut reader = hound::WavReader::open(path).unwrap();

        let samples: Vec<i16> = reader.samples().map(|s| s.unwrap()).collect();
        let slice_samples = samples.clone();

        let len = slice_samples.len();

        assert_eq!(samples, slice_samples);

        WavSlice { samples: samples, slice_samples: slice_samples, len: len}
    }

    fn apply_repeat(self: &mut Self, repeats: usize) {
        if repeats < 2 {
            return
        }
        for _ in 0..repeats-1 {
            self.slice_samples.append(&mut self.slice_samples.clone());
        }
        self.len = self.slice_samples.len();
    }

    fn apply_speed_change(self: &mut Self, speed: f32) {
        if speed == 0.0 {
            return
        }
    }

    fn apply_slice(self: &mut Self, start: usize, end: usize) {
        if start == end {
            return
        }

        else if end < start {
            self.slice_samples = self.slice_samples[end..start].to_vec();
        }
        else if end > start {
            self.slice_samples = self.slice_samples[start..end].to_vec();
        }
        self.len = self.slice_samples.len();
    }
    fn write(self: &Self, _path: &'static str) {
        let spec = hound::WavSpec {
            channels: 1,
            sample_rate: 44100,
            bits_per_sample: 16,
            sample_format: hound::SampleFormat::Int,
        };

        let path: &Path = _path.as_ref();
        let mut writer = hound::WavWriter::create(path, spec).unwrap();
        
        for s in self.slice_samples.clone() {
            writer.write_sample(s).unwrap();
        }
        writer.finalize().unwrap();
    }

    fn reset_buffer(self: &mut Self) {
        self.slice_samples = self.samples.clone();
        self.len = self.slice_samples.len();
    }
}

fn main() {
    let mut wav = WavSlice::new("input/piano.wav");

    // double len
    wav.apply_repeat(2);
    wav.write("slice/test1.wav");

    wav.reset_buffer();

    // reset len
    wav.apply_slice(0, wav.len/5 as usize);
    wav.write("slice/test2.wav");

    wav.reset_buffer();

    // reset len
    wav.reset_buffer();
    wav.write("slice/test4.wav");
}
