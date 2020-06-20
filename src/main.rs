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
    let original_len = wav.len;

    // double len
    wav.apply_repeat(2);
    let double_len = wav.len;
    assert_eq!(original_len*2, double_len);
    wav.write("slice/test1.wav");

    // reset len
    wav.reset_buffer();
    println!("Done! size: {}", wav.len);
    let reset_len = wav.len;
    assert_eq!(reset_len, original_len);
    wav.write("slice/test2.wav");
}