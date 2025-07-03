#!/bin/bash

# Configuration
input_dir="random_3s_per_10s_chunk"  # Input directory containing .flac files
outdir="downsampled_24kHz_wavs_3s_per_10s_chunk" # Output directory for converted WAV files
mkdir -p "$outdir"

JOBS=$(nproc)
echo "Starting downsampling with $JOBS parallel jobs..."

# Conversion function
convert_file() {
    filepath="$1"
    outdir="$2"

    filename=$(basename "$filepath")
    basename_noext="${filename%.*}"

    outname="${outdir}/${basename_noext}.wav"

    # Convert and downsample to 24 kHz WAV
    ffmpeg -hide_banner -loglevel error -i "$filepath" -ar 24000 "$outname"

    if [ $? -eq 0 ]; then
        echo "Converted: $outname"
    else
        echo "Failed: $filepath"
    fi
}

export -f convert_file

# Find all .flac files and run conversions in parallel
find "$input_dir" -type f -name "*.flac" | parallel -j "$JOBS" convert_file {} "$outdir"

echo "Downsampling completed."
echo "Total converted files: $(find "$outdir" -name '*.wav' | wc -l)"
