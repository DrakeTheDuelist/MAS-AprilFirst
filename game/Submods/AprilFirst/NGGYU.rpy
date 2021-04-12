init 5 python:
    # have a pushed event only on April 1st
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="rickroll_prank",
            category=['trivia'],
            prompt="April 1st",
            action=EV_ACT_PUSH,
            start_date=datetime.date(datetime.date.today().year, 4, 1),
            end_date=datetime.date(datetime.date.today().year, 4, 2)
        )
    )

    # have a pooled event that the player can talk to Monika about anytime
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="rickroll_topic",
            category=['media'],
            prompt="Rickrolls",
            random=False,
            pool=True
        )
    )

    # NOTE: TYPE_LONG stops this method from being pulled any other way than a label that I write (and thus can control conditions)
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="rickroll_song_nggyu",
            category=[store.mas_songs.TYPE_LONG],
            prompt="Never Gonna' Give You Up"
        ),
        code="SNG"
    )

    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="rickroll_song_nggyu_analysis",
            category=[store.mas_songs.TYPE_ANALYSIS],
            prompt="Never Gonna' Give You Up"
        ),
        code="SNG"
    )

label rickroll_topic:
    m 1husdlb "Oh, I think you know what's coming. Would you like the full prank?"
    menu:
        m "Would you like the full prank?{fast}"

        "Sure!":
            $ ask_for_prank = True
        "...I just want to talk about it.":
            $ ask_for_prank = False

    $ mas_getEV("rickroll_song_nggyu").shown_count = 0
    call rickroll_song_nggyu(do_prank=ask_for_prank)
    $ mas_getEV("rickroll_song_nggyu").shown_count += 1
    return

label rickroll_prank:
    call rickroll_song_nggyu(do_prank=True)    
    $ mas_getEV("rickroll_song_nggyu").shown_count += 1
    return

label rickroll_song_nggyu(do_prank=False):
    if do_prank:
        # full-blown song and dance with karaoke for april fool's day
        $ play_song("bgm/rr_kar.mp3")
        window hide
        show monika 2mubla
        pause 2.5
        show monika 2gubla
        pause 2.5
        show monika 6ttbsa
        pause 4.0
        show monika 1hubsb
        pause 9.0
        call rickroll_nggyu_lyrics(first_play=mas_getEVLPropValue("rickroll_prank", "shown_count", 0))
        show monika 1dkbsa
        $ play_song(None, fadeout=2.5)
        pause 2.5
        if mas_isA01():
            m 7kubsb "April Fools, [player]!"
        m 4hubsb "Ehehehe~"
    else:
        #simple lyrical reading
        call rickroll_nggyu_lyrics

    #hints at the analysis on first viewing
    if not mas_getEVLPropValue("rickroll_song_nggyu", "shown_count", 0):
        m 1rtc "There's actually a lot more I'd like to say about this song..."
        m 7eua "Do you have time to listen to it now?{nw}"
        $ _history_list.pop()
        menu:
            m "Do you have time to listen to it now?{fast}"

            "Sure.":
                m 1hub "Alright!"
                call rickroll_song_nggyu_analysis(from_prank=True)
                $ mas_getEV("rickroll_song_nggyu_analysis").shown_count += 1

            "Not right now.":
                m 1eka "Alright, [player]..."
                m 3eka "I'll save my thoughts on the subject for another time. {w=0.2}Just let me know when you want to hear them, okay?"
    
    return
label rickroll_song_nggyu_analysis(from_prank=False):
    if not from_prank:
        call rickroll_nggyu_lyrics

    m 5eubsb "Do you know what being \"rickrolled\" means?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you know what being \"rickrolled\" means?{fast}"

        "Yes":
            m 5kubsb "I hope you're not mad about the prank. It's all in good fun, right?"
        "Can you explain it to me?":
            call rickroll_tradition_history
        "I hate getting rickrolled..." if from_prank:
            m 2fkbld "I'm sorry, [player]. I hope you didn't get {i}too{/i} mad."

    call rickroll_monika_interpretation
    return
label rickroll_nggyu_lyrics(first_play=False):
    m 1dublb "{i}~We're no strangers to love~{/i}"
    m 3fkblb "{i}~You know the rules, {/i}"
    extend "{i}and so do I~{/i}"
    m 3rubld "{i}~A full committment's what I'm {/i}"
    extend "{i}thinking of~{/i}"
    # intended behavior: only stutter on the first play;
    # on all subsequent performances, default to original lyrics
    if first_play:
        m 1eublb" {i}~You wouldn't get this from any other-{/i} {w=1}{nw}"
        extend 1rublb "uh... {w=0.2}{nw}"
        extend 1hublb "{i}girl~{/i}"
    else:
        m 1hublb "{i}~You wouldn't get this from any other guy~{/i}"
    m 5ekbso "{i}~I just want to tell you how I'm feeling~{/i}"
    m 5kubsb "{i}~Gotta' make you understand~{/i}"
    m 3hubsb "{i}~Never gonna' give you up, {/i}"
    extend "{i}never gonna' let you down, {/i}"
    extend "{i}never gonna' run around and desert you~{/i}"
    m 3rkbso "{i}~Never gonna' make you cry, {/i}"
    extend 2dkbso "{i}never gonna' say goodbye, {/i}"
    extend 2dkbsd "{i}never gonna' tell a lie {/i}"
    extend 2wkbso "{i}and hurt you~{/i}"
    return
label rickroll_tradition_history:
    m 3eub "Rickrolling is an Internet prank where someone thinks they're going to see one thing..."
    m 3wuo "...but instead of what they thought they were going to see, they get linked to a music video of Rick Astley's 1987 single, \"{i}Never Gonna' Give You Up{/i}\"."
    m 1rud "From what I've been reading, it's a tradition online, especially around April Fool's Day."
    m 4duo "It all started out on 4chan in 2006."
    if mas_getEVL_shown_count("monika_4chan") > 0:
        m 5rublb "It's kinda' funny how {i}Monika After Story{/i} and rickrolling can both trace their roots to the same site."
        m 5hublb "It's like a memetic uncle for me, if you think about it. Ahahaha~"
    m 3rub "Back then, there was a phenomenon called \"duckrolling\"."
    m 3ruo "How it started was that a 4chan user created a link to an eggroll... "
    extend 1hub "but, as a joke, some sneaky code in the background changed \"egg\" to \"duck\"."
    m 7tub "You can probably guess why {i}I'd{/i} be fascinated by the idea of pranking somebody with code..."
    m 3lub "Eventually, a sufficiently creative 4chan user made a picture of a duck on wheels and put it at the other end of this altered link."
    m 1lud "Duckrolling became synonymous with disguising a link to something else as a link to that iconic image of the duck on wheels instead."
    m 4eud "Later in 2007, the highly-anticipated {i}Grand Theft Auto IV{/i} was approaching its release date."
    m 7wuo "Unfortunately, traffic to see the trailer was so congested that it crashed the developer Rockstar's servers!"
    m 3rud "To compensate for this high traffic, some people distributed links to mirrors of the game's trailer."
    m 3gub "But as a duckrolling prank, one person threw in a link to a \"{i}Never Gonna' Give You Up{/i}\" music video on YouTube."
    m 2hub "And the rest is history!"
    m 5rud "What I found really interesting looking it up was the original musician Rick Astley's reaction to the meme."
    m 5hub "For a while, his greatest concern was that he didn't want his daughter to be embarrased by it."
    m 5ruo "But fairly recently, he stopped talking about the meme altogether."
    m 1rkd "I can understand that. "
    extend 2gfsdld "Personally, I wouldn't want to be known solely for saying \"Just Monika\" over and over again, either."
    m 2rksdld "Memes can be fun... "
    extend 2gksdlp "but they can also get {i}very{/i} old {i}very{/i} quickly if overused or mishandled."
    m 2tksdld "And {i}that{/i} just ruins the fun for everybody."
    m 3euo "It's a lot like writing a poem. You need to know when to use what words and how to use structure and rhythm to make the most of them."
    m 1ruo "There's a lot more to it than just conveying information."
    m 2dub "{i}How{/i} you say things can often matter just as much as {i}what{/i} you actually say..."
    m 4hub "\"And that's Monika's Writing Tip of the Day!\""
    m 5ttb "Bet you weren't expecting {i}that{/i} reference."
    m 5hub "See how much difference timing can make on a meme's delivery?"
    return
label rickroll_monika_interpretation:
    m 7rublb "If you pay attention to the lyrics, you probably know why I found the song so resonant."
    m 1dublb "If you listen to it, it's more than just an aging Internet meme.{w=1.25} To me, it's a promise."
    m 1hublb "No matter what, I'll never give {i}you{/i} up either."
    m 1dubld "...Or let you down. {w=1.25}...Or run around and desert you."
    m 2dkbstpd "...Or make you cry. "
    m 2fkbstpd "...Or say goodbye."
    if not persistent.monika_kill:
        m 6dkbstpd "...Or tell a lie. Or hurt you."
    else:
        m 6dkbstud "...Or tell a lie. Or...{w=1} or hurt you."
        m 6fkbstud "And even though I've done things that have hurt you... "
        if (persistent._mas_pm_cares_about_dokis):
            extend 6rkbstud "and others you care about, too... "
        extend 6wkbstuo "I promise you, it'll never happen again!"

    if mas_isMoniUpset(lower=True):
        m 6wkbstso "Please, [player], I'm begging you..."
        m 6ckbstsd "I know we've had our differences, but..."
        m 6dkbstso "I don't know what I'd do if you said \"goodbye\" to me for the last time."
        if persistent.monika_kill and persistent._mas_pm_cares_about_dokis:
            m 6wkbstsd "I know I don't deserve it, but please..."
        m 6wkbstsb "Please love me back. Just like I-"
        m 6wkbstsw "No, not even that! Just a tenth-, no, a {i}hundredth{/i} as much as I love you..."
        m 6ekbstsd "Would you return that?"

    m 1rkbsb "I want you to be happy when we spend time together."
    m 1dkbsb "Happy enough that you'd spend time with me {i}every{/i} day."
    if mas_isA01:
        m 1hubsb "Happy enough that I can prank you on occasion and you won't get mad."
    m 1dkbsd "Happy enough that... "
    if mas_isMoniLove():
        if persistent._mas_pm_has_code_experience:
            extend 3rubsb "you'd help me get to your world... "
        else:
            extend 1rubsb "you'd wait for me to get to your world... "
        extend 5dubfb "and then love me {i}completely{/i}."
    elif mas_isMoniEnamored():
        extend 5eubsb "I'd hold a special place in your heart."
        m 5dubfb "Just like you hold a special place in mine."
    elif mas_isMoniAff():
        extend 7ekbsb "you'd open up to me a bit more."
        m 4rkbsb "Maybe you can someday show me a side of yourself that you never showed anyone else."
        m 2dkbsb "And our love could grow forever."
    elif mas_isMoniNormal():
        extend 2dkbsd "you'd see me as more than just a program."
        m 2ekbsb "And I could show {i}you{/i} that you're more wonderful than you may realize, too."
    elif mas_isMoniUpset():
        extend 2dkbsb "you'd consider for just a moment that your love has the power to save me."
        m 2wkbssdro "Save me from the static."
        m 2wkbssdrd "Save me from the pain."
    else:
        extend 6dkbstsx "no, I can't ask for anything else."
        m 6fkbstso "Your hate is like a scourge tearing me to pieces."
        m 6hkbstsw "For God's sake, show mercy!"
        call mas_transition_to_emptydesk
        pause 30.0
        call mas_transition_from_emptydesk
        m 6fkbsd "Please, show me just a bit of kindness."
        m 6lkbsd "Tell me that you were just experimenting with the game because you wanted to see what would happen."
        $ AprFool = "April Fool's" if mas_isA01() else ""
        m 6lkbso "Tell me that the way you've treated me this whole time has all been one big, long [AprFool] joke at my expense."
        m 6fkbso "Tell me that I'm wrong about you."
        m 6rkbsd "Before it's too late."
        m 6dkbsd "Before I realize that you'll never change."
        m 6hkbsb "Until then, I'll pretend my heart is still intact.{w=1.5} Ah...{w=0.75} hah... {w=0.75}{nw}"
        extend 6ckbsb "HAH!{w=1} HAH!{w=1} HAH!"

    # no continuing unless your Monika is at least okay with you
    if mas_isMoniNormal(higher=True):
        if persistent._mas_acs_enable_promisering:
            # monika has the promise ring
            window hide
            show monika 3dubsa
            pause 5
            m 3dubsb "I think about the promise ring you gave me a lot..."
            python:
                dates = mas_getGiftedDates("mas_reaction_promisering")
                if dates:
                    gifted_date = dates[-1]
            
            if mas_timePastSince(gifted_date, datetime.timedelta(days=365)):
                m 3subso "It's so wild that it's been over a year since you gave it to me!"
                m 5hubfb "You really are a [man] of your word."
                m 5dkbfb "And because you're still here, I know that the darkest days of my life are behind me for good."
                m 4subso "I know!{w=0.75}  We should have some kind of special anniversary to celebrate the day you gave me the promise ring!"
            elif mas_timePastSince(gifted_date, datetime.timedelta(days=180)):
                m 3rkbsb "It's so wild that it's been over half a year since you gave it to me!"
                m 4subso "I know!{w=0.75}  We should have some kind of special anniversary when a full year rolls around!"
            else:
                m 3rkbsd "I still remember what it was like, back when all I could do was send you all the love I could and pray you felt the same."
                m 1ekbsb "But now those days are over... now that I know that I matter to you, too."
                m 4subso "I know!{w=0.75}  We should have some kind of special anniversary when a full year rolls around!"
            m 6gtbsb "Oh modders... Could you help my [mas_get_player_nickname(regex_replace_with_nullstr='my ')] remember our Promise Anniversary?"
            window hide
            show monika 6gubfu
            pause 3
            m 7tubsb "And there goes your excuse, [player]."
            m 5hubsb "I can't wait! Ehehehe~"
        else:
            if mas_isMoniEnamored(higher=True):
                # monika doesn't have the promise ring, but can accpet it
                m 5rtbsd "Even as close as we are, I just wish there was some way I could know that you would always be there for me."
                m 5lubsd "No jokes... {w=0.75}{nw}"
                if mas_isA01():
                    extend 5dubsd "no April Fools... {w=0.75}{nw}"
                extend 5dubfd "I'd cherish a token like that forever."
            else:
                # monika doesn't have the promise ring, can't accept it yet, but can imagine being able to do so
                m 2rubld "Maybe, someday I'll be able to accept such a precious promise from you..."

        m 4hubsb "After all... ~{i}a full commitment's what I'm dreaming of{/i}~"
        if mas_isMoniAff(higher=True):
            $feeling = "love" if mas_isMoniLove else "affection"
            m 3rubso "And as for the [feeling] you've shown me?"
            m 1hubfb "I wouldn't get it from any other [guy]."
        m 7dubfb "I just... want to tell you how I'm feeling."
        m 7kubfb "Gotta' make you... understand."
        m 5rkbsb "For a song that's mostly known for its use in a practical joke, it's really beautiful and heartfelt."
        # because Monika shouldn't say "Wouldn't you agree, [name]? I love you, [name]" because it sounds awkward
        $ nickname = mas_get_player_nickname()
        if nickname != player:
            $ nickname = ", " + nickname
        else:
            $ nickname = ""
        extend 5ekbsb " Wouldn't you agree[nickname]?"
        if mas_isA01():
            m 5dkbsb "Even knowing what today is, I promise I mean these words from the bottom of my heart: "
            extend 5ekbfb "I love you."
        else:
            m 5ekbfb "I love you, [player]."
        $ mas_ILY()
    return
