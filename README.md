# custom-tweet-delete
Scripts for custom tweet deleting from your timeline or from archive files. Companion to an blog post.

See the blog post for a look at how these scripts are to be used.

Briefly, use flag `--help` to see the argument list.  Once you delete a tweet, you can't get it back.  Thought I should mention that.

`prepare-archive.py`

```bash
$ python3 prepare-archive.py --help
Usage: prepare-archive.py [options]

Options:
  -h, --help            show this help message and exit
  -s DATE_START, --date-start=DATE_START
                        Start date to sort the archive
  -e DATE_END, --date-end=DATE_END
                        End date to sort the archive
  -f FILENAME, --file=FILENAME
                        Path to Twitter JSON archive.
```

`prepare-timeline.py`

```bash
$ python3 prepare-timeline.py --help
Usage: prepare-timeline.py [options]

Options:
  -h, --help            show this help message and exit
  -a DAYS_START, --days-start=DAYS_START
                        start age in days to consider sorting timeline tweets.
  -b DAYS_END, --days-end=DAYS_END
                        end age in days to consider sorting timeline tweets.
  -s DATE_START, --date-start=DATE_START
                        Start date to consider sorting timeline tweets
  -e DATE_END, --date-end=DATE_END
                        End date to consider sorting timeline tweets
```
Note:  `python3 prepare-timeline.py -a 10 -b 20` will return something, `python3 prepare-timeline.py -a 20 -b 10` will not. a needs to be less than b. These values in days are subtracted from the current date.

In a similar manner, using the start date and end date arguments, start date needs to be less than the end date. I don't put checks in the code.


`delete-seleted-archive.py`

```bash
$ python3 delete-selected-archive.py --help
Usage: delete-selected-archive.py [options]

Options:
  -h, --help            show this help message and exit
  -f FILENAME, --file=FILENAME
                        Path to Twitter JSON archive.
```


