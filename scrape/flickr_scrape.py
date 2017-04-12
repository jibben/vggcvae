import flickrapi
import urllib
from secret import API_KEY, API_SECRET

DIR = './flickr/'
PREFIX = 'http://farm{farm}.staticflickr.com/{server}/'
SUFFIX = '{id}_{secret}_b.jpg'

def get_photo(photo, save_dir=DIR):
    url = (PREFIX + SUFFIX).format(**photo)
    local = save_dir + SUFFIX.format(**photo)

    with urllib.request.urlopen(url) as res, open(local, 'wb') as fout:
        fout.write(res.read())

def scrape_tag(flickr, tags):
    tag = ','.join(tags)
    per_page = '100'
    save_dir = DIR + ('%s/' % '-'.join(tags))

    photos = flickr.photos.search(per_page=per_page, tags=tag, page='1')

    if photos['stat'] != 'ok':
        print(photos['stat'])
        raise ValueError(photos['stat'])

    pages = photos['photos']['pages']
    total = photos['photos']['total']

    processed = 0

    for i in range(1, pages):
        photos = flickr.photos.search(per_page=per_page, tags=tag, page=str(i))

        for photo in photos['photos']['photo']:
            processed += 1
            get_photo(photo, save_dir)

        if i % 10 == 0:
            print('%d / %d' % (i * 100, total))

    return processed

def scrape_group(flickr, group_id, group_name, per_page=100):
    save_dir = DIR + group_name + '/'

    photos = flickr.groups.pool.getPhotos(group_id=group_id, per_page = per_page, page='1')

    if photos['stat'] != 'ok':
        print(photos['stat'])
        raise ValueError(photos['stat'])

    pages = photos['photos']['pages']
    total = photos['photos']['total']

    processed = 0

    for i in range(1, pages):
        photos = flickr.groups.pool.getPhotos(group_id=group_id, per_page = per_page, page='1')

        for photo in photos['photos']['photo']:
            processed += 1
            get_photo(photo, save_dir)

        if i % 10 == 0:
            print('%d / %d' % (i * 100, total))

    return processed

def main():
    flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, format='parsed-json')

    watercolorpaintings = '431249@N22'
    tags = ['watercolor', 'watercolour']

    scrape_group(flickr, watercolorpaintings, 'watercolorpaintings')

if __name__ == '__main__':
#    main()
    print(API_KEY)
    print(API_SECRET)
