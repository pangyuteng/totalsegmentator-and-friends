FROM wasserth/totalsegmentator_container:master

# getting below permission error in htcondor+docker
RUN mkdir -p /nonexistent/.totalsegmentator && chmod -R 777 /nonexistent

# # maybe below will trick docker to cache the weights?
# COPY blank.nii.gz /tmp/blank.nii.gz
# RUN TotalSegmentator -i /tmp/blank.nii.gz -o /tmp/blank-seg