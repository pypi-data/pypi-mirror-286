if [[ -z ${NO_CLEAN} ]]; then
  cd /tmp && rm -rf .venv && python -m venv .venv && . .venv/bin/activate && cd ~/sdrterm \
    && PIP_NO_BINARY="" pip install . --upgrade;
fi

if [[ -z ${DSD_CMD} ]]; then
  DSD_CMD="dsd -q -i - -o /dev/null -n";
fi

if [[ -z ${OUT_PATH} ]]; then
  OUT_PATH=/tmp;
fi

if [[ -z ${SDRTERM_EXEC} ]]; then
  SDRTERM_EXEC="python -m sdrterm";
fi

export DSD_CMD="$DSD_CMD";
export OUT_PATH="$OUT_PATH";
export SDRTERM_EXEC="$SDRTERM_EXEC";

echo "$OUT_PATH";
echo "$DSD_CMD";
echo "$SDRTERM_EXEC";

setBlue=$(tput setaf 1);# interestingly, red = R|G|B = 1|0|0.
setNormal=$(tput sgr0);

declare -A sums;

sums["${OUT_PATH}/outB.wav"]="86c5e57ffd7319483165bd230f5da35e";
sums["${OUT_PATH}/outd-B.wav"]="b4dd2ad8708c7316cdee04da0d8c56a6";
sums["${OUT_PATH}/outd.wav"]="b4dd2ad8708c7316cdee04da0d8c56a6";
sums["${OUT_PATH}/outf-B.wav"]="cea79d9beef0bb5ecfdd8dfd1235e62b";
sums["${OUT_PATH}/outf.wav"]="cea79d9beef0bb5ecfdd8dfd1235e62b";
sums["${OUT_PATH}/outh-B.wav"]="d7c25d6165ae4f4b223b2ccd6a5869d5";
sums["${OUT_PATH}/outh.wav"]="d7c25d6165ae4f4b223b2ccd6a5869d5";
sums["${OUT_PATH}/outi-B.wav"]="cea79d9beef0bb5ecfdd8dfd1235e62b";
sums["${OUT_PATH}/outi.wav"]="cea79d9beef0bb5ecfdd8dfd1235e62b";
sums["${OUT_PATH}/outi16.wav"]="41b60c8104815d1830db3f2c0ecc1777";
sums["${OUT_PATH}/outi16X.wav"]="41b60c8104815d1830db3f2c0ecc1777";
sums["${OUT_PATH}/outu8.wav"]="b49c2a9207a62a196cc60c44c155200e";
#sums["${OUT_PATH}/outB.wav"]="b8058749ff0e25eab70f92dda86c2507";
#sums["${OUT_PATH}/outd.wav"]="d51e36787d2cf8a10be87a1e123bb976";
#sums["${OUT_PATH}/outf.wav"]="07e31be2ff4f16b91adcf540a570c03e";
#sums["${OUT_PATH}/outh.wav"]="576409e4a3cd5e76950aa0134389d75a";
#sums["${OUT_PATH}/outi.wav"]="07e31be2ff4f16b91adcf540a570c03e";

#sums["${OUT_PATH}/outd-B.wav"]="d51e36787d2cf8a10be87a1e123bb976";
#sums["${OUT_PATH}/outf-B.wav"]="07e31be2ff4f16b91adcf540a570c03e";
#sums["${OUT_PATH}/outh-B.wav"]="576409e4a3cd5e76950aa0134389d75a";
#sums["${OUT_PATH}/outi-B.wav"]="07e31be2ff4f16b91adcf540a570c03e";

#sums["${OUT_PATH}/outi16.wav"]="9f21f81dd274b3695adbb0418f787b48";
#sums["${OUT_PATH}/outu8.wav"]="18f1c6cbe373121a3f4c1bfe9f282467";

function cleanup {
  for i in "${!sums[@]}"; do
    if [[ $i == *"tmp"* ]]; then
      rm "$i";
    fi
  done
  deactivate 2>&1 > /dev/null;
}
trap cleanup EXIT;

TEMP=$DSD_CMD
export DSD_CMD="${DSD_CMD} -f1";
coproc SIMO {
  time ./example_simo_file.sh -i /mnt/d/uint8.wav --vfos=15000,-60000 -w5k -c-3.5E+5 -t155.685M -vv -d64 2>&1
}

ts="";
while IFS= ; read -r line; do
  if [[ $line == *"real"* ]] || [[ $line == *"user"* ]] || [[ $line == *"sys"* ]]; then
    echo $line;
  elif [[ $line == *"timestamp"* ]]; then
    ts=$(echo $line | grep "timestamp" - | sed -E "s/^.*: timestamp: ([0-9]+)$/\1/g");
    echo "${OUT_PATH}/out-155625000-${ts}.wav";
    echo "${OUT_PATH}/out-155685000-${ts}.wav";
    echo "${OUT_PATH}/out-155700000-${ts}.wav";
  fi
done <&"${SIMO[0]}"

sums["${OUT_PATH}/out-155625000-${ts}.wav"]="434485a583b033f7719d16abd808cb52";
sums["${OUT_PATH}/out-155685000-${ts}.wav"]="9e2398fe90d43318f9a3a7797792aed4";
sums["${OUT_PATH}/out-155700000-${ts}.wav"]="66d03fda1b8a07e00fd75cbc992715de";
#sums["${OUT_PATH}/out-155625000-${ts}.wav"]="38acd5677b3e813eea185523d47b9076";
#sums["${OUT_PATH}/out-155685000-${ts}.wav"]="4cae5a0dfbbe4bd06ea4de41988bd606";
#sums["${OUT_PATH}/out-155700000-${ts}.wav"]="2eaa5e1e736f3b68e67c3b89d1407e1e";

wait $SIMO_PID;
ret=${?};
echo "sdrterm returned: ${ret}";
export DSD_CMD="${TEMP} -fr";

./example.sh /mnt/d/SDRSharp_20160101_231914Z_12kHz_IQ.wav;

declare -A z="( `sed -E "s/^((\d|\w)+)\s*((\d|\w|\/|\-|\.)+)$/[\3]=\1/g" <<< $(md5sum ${OUT_PATH}/*.wav)` )";
for i in "${!sums[@]}"; do
  if [[ "${sums["$i"]}" == "${z["$i"]}" ]]; then
    echo "checksum matched: ${i}"
  else
    printf "${setBlue}FAILED: ${i}\n\tEXPECTED: ${sums["$i"]}\n\tRECEIVED: ${z["$i"]}\n${setNormal}" 1>&2;
  fi
done

rm -rf /tmp/.venv;
exit $ret;
