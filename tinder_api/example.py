import session
import itertools
from datetime import datetime
import os
import wget

sess = session.Session() # inits the session

print("My _id is %s" %sess.get_id())

#sess.update_profile(bio="VIM is the best")


def download_image(imageList, name, ddir):
    """ This function takes in a list of images, along with a name for the 
        output and downloads them into a directory.
    """
    for i, image in enumerate(imageList):
        wget.download(image, out= ddir + str(name + '_' +str(i)) + '.jpg')

for user in itertools.islice(sess.yield_users(), 1):
    print(user.name) # prints the name of the user see __init__
    # How to check if it exists, if it doesnt, it returns <MisssingValue>
    if user.bio is not "<MissingValue>":
        print(user.bio)
    # print(user.like()) # returns false if not a match
    print(user.photos)
    #download_image(user.photos, user.name)


#for match in sess.yield_matches():
#    print(match.name)
#    print(match.match_data) # prints all the match_data
#    print([x.body for x in match.get_messages()]) # gets the body of messages
    #print(match.message("Hello")) # sends hello to the match


