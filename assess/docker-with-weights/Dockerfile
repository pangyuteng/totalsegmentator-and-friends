FROM wasserth/totalsegmentator_container:master
# maybe below will trick docker to cache the weights?
COPY blank.nii.gz /tmp/blank.nii.gz
RUN TotalSegmentator -i /tmp/blank.nii.gz -o /tmp/blank-seg