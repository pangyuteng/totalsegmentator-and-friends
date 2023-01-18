FROM wasserth/totalsegmentator_container:master

#
# download weights! https://github.com/wasserth/TotalSegmentator/blob/bc865436188c68fff55dadff4aaa8940a96609e5/totalsegmentator/libs.py#L77
# download_weights.py copied from # copied from /opt/conda/lib/python3.6/site-packages/totalsegmentator/download_pretrained_weights.py

ENV TOTALSEG_WEIGHTS_PATH=/opt/totalsegmentator_weights

# in addition to original task ids, added 258 for `-ta lung_vessels`
ARG TASK_ID_LIST="[251,252,253,254,255,256,258]"

RUN mkdir -p /opt/totalsegmentator_weights
WORKDIR /opt
COPY download_weights.py /opt/download_weights.py
RUN python /opt/download_weights.py
RUN chmod 777 /opt/totalsegmentator_weights