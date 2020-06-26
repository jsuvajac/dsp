use std::path::Path;


#[derive(Debug, Clone)]
pub struct WavSlice {
    samples: Vec<i16>,
    pub slice_samples: Vec<i16>,
    pub len: usize
}

impl WavSlice {
    pub fn new(path: &'static str) -> WavSlice {
        let mut reader = hound::WavReader::open(path).unwrap();

        let samples: Vec<i16> = reader.samples().map(|s| s.unwrap()).collect();
        let slice_samples = samples.clone();

        let len = slice_samples.len();

        assert_eq!(samples, slice_samples);

        WavSlice { samples, slice_samples, len}
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
        } else if speed < 0.0 {
            self.apply_reverse();
        }

        if speed.abs() >= 1.0 {
            let factor = speed.abs() as usize;
            //println!("speed factor: {}", factor);
            self.slice_samples = self.slice_samples.clone()
                                                   .into_iter()
                                                   .enumerate()
                                                   .filter(|&(i, _)| i % factor == 0 )
                                                   .map(|(_, e)| e)
                                                   .collect::<Vec<_>>();
        } else if speed.abs() > 0.0 {
            let factor = (1.0 / speed.abs()) as usize;
            //println!("slowdown factor: {}", factor);
            self.slice_samples = self.slice_samples.clone()
                                        .into_iter()
                                        .map(|e| vec![e; factor])
                                        .flatten()
                                        .collect::<Vec<_>>();
        }
        self.len = self.slice_samples.len();
    }

    fn apply_reverse(self: &mut Self) {
        self.slice_samples.reverse();
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

#[derive(Debug)]
pub struct ReadHead {
    slice: WavSlice,
    index: usize,
    pub playing: bool
}

impl ReadHead {
    pub fn new(wav: WavSlice) -> ReadHead {
        ReadHead{slice: wav, index: 0 as usize, playing: false}
    }
    pub fn get_index(self: &mut Self) -> usize {
        self.index
    }
    pub fn get_next(self: &mut Self) -> i16 {
        let next = self.slice.slice_samples[self.index];
        self.index = (self.index + 1) % self.slice.len;
        next
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn repeat() {
        let mut wav = WavSlice::new("input/piano.wav");
        let original_len = wav.len;

        // * 2 len
        wav.apply_repeat(2);
        let double_len = wav.len;
        assert_eq!(original_len*2, double_len);

        // * 4 len
        wav.apply_repeat(2);
        let quad_len = wav.len;
        assert_eq!(original_len*4, quad_len);
    }

    #[test]
    fn speed() {
        let mut wav = WavSlice::new("input/piano.wav");
        let original_len = wav.len;


        // half speed
        wav.apply_speed_change(-0.25);
        assert_eq!(original_len*4, wav.len);

    }

    #[test]
    fn reset() {
        let mut wav = WavSlice::new("input/piano.wav");
        let original_len = wav.len;

        wav.apply_slice(0, wav.len/5);
        wav.apply_slice(0, wav.len/5);

        wav.reset_buffer();

        assert_eq!(original_len, wav.len);
    }

    #[test]
    fn write() {
        use std::fs;
        use std::path::Path;

        let mut wav = WavSlice::new("input/piano.wav");
        wav.apply_slice(0, 5);
        wav.write("input/test_slice.wav");

        assert!(Path::new("input/test_slice.wav").exists());
        fs::remove_file("input/test_slice.wav");
    }

    #[test]
    fn slice() {
        let mut wav = WavSlice::new("input/piano.wav");
        let original_len = wav.len;

        wav.apply_slice(0, wav.len/5);
        assert_eq!(original_len/5, wav.len);
        assert_eq!(wav.slice_samples, wav.samples[..wav.samples.len()/5].to_vec());
    }

    #[test]
    fn reverse() {
        let mut wav = WavSlice::new("input/piano.wav");
        let original_len = wav.len;

        // reset len
        wav.apply_reverse();
        wav.samples.reverse();
        assert_eq!(wav.slice_samples, wav.samples);
        assert_eq!(wav.len, original_len);
    }

    #[test]
    fn read_head() {
        let wav = WavSlice::new("input/piano.wav");
        let mut head = ReadHead::new(&wav);

        for i in 0 .. 5 {
            //println!("{} -> {}", head.get_index(), head.get_next());
            //println!("{} -> {}", i, wav.slice_samples[i]);
            assert_eq!(head.get_next(), wav.slice_samples[i]);
        }
    }


}