# satdatagen
a Python package for generating datasets to be used in satellite tasking schedulers

## User Requirements
This package relies on data collected from space-track.org, one of the main resource for satellite ephemeral data. Users of satdatagen must have an existing space-track.org login. Add a file called `credentials.json` to your working directory, with login information formatted as a JSON object:

```
{
  identity : 'username@email.com',
  password : 'yourPassword12345'
}
```

The satdatagen code will query the space-track.org servers for satellite data using the user's login information.  Note that each user is subject to space-track's query limit - up to 30 queries per minute and up to 300 queries per hour.  
