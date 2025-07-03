#!/bin/bash

# Configuration
input_dir="data/datasets/nouragues_19-23/2019/Data"  # Input directory containing .flac files
outdir="random_3s_per_10s_chunk"                # Output directory for test chunks
mkdir -p "$outdir"

JOBS=$(nproc)
echo "Début du traitement avec $JOBS jobs..."

# Processing function with re-encoding
process_file() {
    filepath="$1"
    outdir="$2"

    filename=$(basename "$filepath")
    basename_noext="${filename%.*}"

    # Get duration using ffprobe
    duration=$(ffprobe -v error -show_entries format=duration \
        -of default=noprint_wrappers=1:nokey=1 "$filepath")

    total_sec=$(printf "%.0f" "$duration")
    n_chunks=$(( total_sec / 10 ))

    if [ "$n_chunks" -eq 0 ]; then
        echo "⚠️ Skipped (too short): $filename"
        return 0
    fi

    for (( i=0; i<n_chunks; i++ )); do
        chunk_start=$(( i * 10 ))
        rand_offset=$(( RANDOM % 8 ))
        start_time=$(( chunk_start + rand_offset ))

        outname="${outdir}/${basename_noext}_chunk${i}_rand3s.flac"

        # Re-encode instead of using -c copy
        ffmpeg -hide_banner -loglevel error -ss "$start_time" -t 3 -i "$filepath" -c:a flac "$outname"
        
        if [ $? -eq 0 ]; then
            echo "Success: $outname"
        else
            echo "Failed: $filename chunk $i"
        fi
    done
}

export -f process_file

find "$input_dir" -type f -name "*.flac" | parallel -j "$JOBS" process_file {} "$outdir"

echo "Terminé."
echo "Total de fichiers générés: $(find "$outdir" -name '*.flac' | wc -l)"
