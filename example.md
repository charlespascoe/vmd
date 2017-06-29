# An Example Markdown Document #

This is an example document! *Lorem ipsum **dolor sit amet**, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.*

# Lists #

## Bullet Points ##

Here's a bullet point list:

* This is a bullet point
* This is another bullet point
    * A sub-bullet point

## Numbered Lists ##

Here's a numbered list:

1. This is the first item in a numbered list
2. This is the second
    1. This is a sub-item in a numbered list
    2. And another
3. And back again!

# Links #

This paragraph has some [links](https://github.com/cpascoe95/vmd) that appear after the paragraph. Links [can *even* have **different** styles within them](https://www.google.co.uk). [Lorem ipsum](http://www.lipsum.com/) dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

# Code #

This paragraph has some `inline code`!

```
import base64


def main():
    b64_message = 'U3ludGF4IGhpZ2hsaWdodGluZyBjb21pbmcgc29vbiE='
    decoded = base64.b64decode(b64_message.encode()).decode()
    print(decoded)


if __name__ == '__main__':
    main()
```

# Horizontal Divider #

---

# Quotes #

Here's a quote:

>   "Test"
>   \- Test

# Headings #

## Heading 2 ##

### Heading 3 ###

#### Heading 4 ####

##### Heading 5 #####

###### Heading 6 ######

## Headings have incrementing counters ##

## And another! ##
