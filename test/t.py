from Mishmash import mishmash

a = mishmash()



print(a._set)
for i in a:
    
    print(i)
    print("------ ")

a["sadf"] = [
    {
      "fixture_id": 100,
      "event_date": "2018-09-01T14:00:00+00:00",
      "home_team":  "Everton",
      "away_team": "Huddersfield",
      "score": {
        "halftime": "1-1",
        "fulltime": "1-1"
      },
      "events": [
  
        {
          "elapsed": 34,
          "player": "Philip Billing",
          "type": "Goal"
        },
        {
          "elapsed": 36,
          "player": "Dominic Calvert-Lewin",
          "type": "Goal"
        }]
    },
    {
      "fixture_id": 101,
      "event_date": "2018-09-01T14:00:00+00:00",
      "home_team":  "Wolves",
      "away_team": "West Ham",
      "score": {
        "halftime": "0-0",
        "fulltime": "0-1"
      },
      "events": [
        
        {
          "elapsed": 90,
          "player": "Adama Traoré",
          "type": "Goal"
        }
      ]
    },
    
    {
      "fixture_id": 102,
      "home_team":  "Manchester City",
      "away_team": "Newcastle",
      "event_date": "2018-09-01T16:30:00+00:00",
      "score": {
        "halftime": "1-1",
        "fulltime": "2-1"
      },
      "events": [
        {
          "elapsed": 8,
          "player": "Raheem Sterling",
          "type": "Goal"
        },
        {
          "elapsed": 30,
          "player": "DeAndre Yedlin",
          "type": "Goal"
        },
        {
          "elapsed": 52,
          "player": "Kyle Walker",
          "type": "Goal"
        }]
    }
  ]