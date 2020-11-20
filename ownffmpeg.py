import subprocess

# -------------------------------------------------- FFMPEG

def ffmpeg_get_audio(file_input, file_output):
    command = f"ffmpeg -y -hide_banner -loglevel warning -i \"{file_input}\" -ab 160k -ac 2 -ar 44100 -vn \"{file_output}\""
    subprocess.call(command, shell=True)

def ffmpeg_cut_array(file_input, file_output, temp_file, timearray):
    # create temp file with filter_complex_script
    full_length = 0
    f = open(temp_file, "w")
    i = 0
    for start, end in timearray:
        full_length += end - start
        f.write(f"[0:v]trim=start={str(start)}:end={str(end)},setpts=PTS-STARTPTS[vpart{i}];")
        f.write(f"[0:a]atrim=start={str(start)}:end={str(end)},asetpts=PTS-STARTPTS[apart{i}];")
        i+=1
    length = i
    i = 0
    for i in range(length):
        f.write(f"[vpart{i}][apart{i}]")
    f.write(f"concat=n={length}:v=1:a=1[vout][aout]")
    f.close()

    # execute script
    command = f"ffmpeg -y -hide_banner -loglevel warning -i \"{file_input}\" -filter_complex_script \"{temp_file}\" -safe 0 -map [vout] -map [aout] -to {full_length} \"{file_output}\""
    # print(command)
    subprocess.call(command, shell=True)

def ffmpeg_cut_from_original(file_input, file_output, start, end):
    command = f"ffmpeg -y -hide_banner -loglevel warning -i \"{file_input}\" -ss {str(start)} -to {str(end)} \"{file_output}\""
    subprocess.call(command, shell=True)

def ffmpeg_combine(file_input, file_output):
    command = f"ffmpeg -y -hide_banner -loglevel warning -f concat -safe 0 -i \"{file_input}\" -c copy \"{file_output}\"" #todo give option to run without -c copy to fully compress (takes longer)
    subprocess.call(command, shell=True)

def ffmpeg_segments(file_input, file_output, segment_seconds):
    command = f"ffmpeg -y -hide_banner -loglevel warning -i \"{file_input}\" -c copy -segment_time {segment_seconds} -f segment \"{file_output}\""
    subprocess.call(command, shell=True)
