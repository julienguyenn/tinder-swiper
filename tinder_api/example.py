import session
import itertools
from datetime import datetime
import os
import wget

sess = session.Session() # inits the session

print("My _id is %s" %sess.get_id())

#sess.update_profile(bio="VIM is the best")


# this function takes in a list of images, along with a name for the output
#  and downloads them into a directory
def download_image(imageList, name):
    # select directory
    os.chdir('C:\\Users\\dnmor\\Documents\\Tinder API\\tinder-swiper\\test')
    count = 1
    for image in imageList:
        local_image = wget.download(image, out= str(name + str(count)) + '.jpeg')
        count += 1

for user in itertools.islice(sess.yield_users(), 10):
    print(user.name) # prints the name of the user see __init__
    # How to check if it exists, if it doesnt, it returns <MisssingValue>
    if user.bio is not "<MissingValue>":
        print(user.bio)
    # print(user.like()) # returns false if not a match
    print('# of photos:', len(user.photos))
    download_image(user.photos, user.name)


#for match in sess.yield_matches():
#    print(match.name)
#    print(match.match_data) # prints all the match_data
#    print([x.body for x in match.get_messages()]) # gets the body of messages
    #print(match.message("Hello")) # sends hello to the match


