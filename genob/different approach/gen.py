# Generate 


import Augmentor


p = Augmentor.Pipeline("data")

p.crop_random(probability=1, percentage_area=0.5)
p.resize(probability=1.0, width=120, height=120)

p.sample(1, multi_threaded=True)