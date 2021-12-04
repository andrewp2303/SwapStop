import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from swapproj.database import db_session
from swapproj.database import (
    Club, Event, ClubEvent, Tag, ClubLeader, Calendar, ClubTag, Signup
)

bp = Blueprint('application', __name__, url_prefix='/')

# Route for club creation
# GET: Displays create club form
# POST: Creates club according to the input from form
@bp.route("/createclub", methods=["GET", "POST"])
def createclub():
    
    # Renders survey for creating a club
    if request.method == "GET":
        newclub = Club(title = "", description = "")
        return render_template("createclub.html", club=newclub)

    # Retrieves all the info and insert into clubs database
    else:

        # Retrieves user input from form
        ctitle = request.form.get("title")
        cdescription = request.form.get("description")
        cmembership_process = request.form.get("membership_process")
        csize = request.form.get("size")
        cis_accepting_members = True if request.form.get("is_accepting_members") == "Yes" else False
        crecruiting_cycle = request.form.get("recruiting_cycle")
        ctime_commitment = request.form.get("time_commitment")

        # Initializes created club info
        newclub = {
            'title': ctitle,
            'description': cdescription,
            'membership_process': cmembership_process,
            'size': csize,
            'is_accepting_members': cis_accepting_members,
            'recruiting_cycle': crecruiting_cycle,
            'time_commitment': ctime_commitment
        }

        # Checks there is input for all desired values
        if (not ctitle or not cdescription or not cmembership_process
                or not csize or not crecruiting_cycle or not ctime_commitment):
            flash("Please provide all inputs!")
            return render_template("createclub.html", club = newclub)
        
        # Make sure multiple clubs do not have same name (Consideration TODO: do not re-enter bad title)
        if db_session.query(Club).filter_by(title = ctitle) != None:
            flash("Title already in use.")
            return render_template("createclub.html", club = newclub)

        else:
            # Add Club
            newclub = Club(
                title = ctitle,
                description = cdescription,
                membership_process = cmembership_process,
                size = csize,
                is_accepting_members = cis_accepting_members,
                recruiting_cycle = crecruiting_cycle,
                time_commitment = ctime_commitment
            )
            db_session.add(newclub)
            db_session.commit()


            # Add club leader
            newclubleader = ClubLeader(
                user_id = session["user_id"],
                club_id = newclub["id"]
            )
            db_session.add(newclubleader)
            db_session.commit()
            flash("Club added!")
            return redirect("/")

# Route for club updating (gets update page, posts update request)
# GET: Displays clubs user is a part of
# POST: Sets session["club_id"] to the selected club
@bp.route("/selectclub", methods=["GET", "POST"])
def selectclub():

    # For testing purposes
    session["user_id"] = 1

    if request.method == "GET":
        # Retrieves all club ids for clubs user leads (Future TODO: Only display clubs where the user is a club leader)
        clubs = db_session.query(Club).all()

        # Checks if user has access 
        if not clubs:
            flash("You Do Not Have Access To This Feature.")
            return redirect("/")

        return render_template("selectclub.html", clubs=clubs)
    
    else:
        
        # Retrieves club from form
        session["club_id"] = int(request.form.get("process"))

        # Finds club info using selected_club
        clubinfo = db_session.query(Club).filter_by(id = session["club_id"]).first()

        # Renders club information in updateclub
        return render_template("/updateclub.html",club=clubinfo)


# Route for club updating (gets update page, posts update request)
# GET: finds current club info and displays it
# POST: updates club according to the input from form
@bp.route("/updateclub", methods=["GET", "POST"])
def updateclub():

    # Renders survey for updating a club
    if request.method == "GET":
        
        # Find and store club id
        uclub = db_session.query(Club).filter_by(id = session["club_id"])

        # Send into render_template and adjust updateclub.html to add jinja
        return render_template("updateclub.html", club=uclub)

    # If form is submitted, get all the info and insert into Club table
    else:
        
        # Checks new club title is taken
        ctitle = request.form.get("title")
        if ctitle == None or db_session.query(Club).filter_by(title = ctitle) == None:
            flash("Title already in use.")
            return redirect("/updateclub")
        
        # Retrives updated info from form
        cdescription = request.form.get("description")
        cmembership_process = request.form.get("membership_process")
        csize = request.form.get("size")
        cis_accepting_members = True if request.form.get("is_accepting_members") == "Yes" else False
        crecruiting_cycle = request.form.get("recruiting_cycle")
        ctime_commitment = request.form.get("time_commitment")

        # Initializes updated club info
        updatedclub = {
            'title': ctitle,
            'description': cdescription,
            'membership_process': cmembership_process,
            'size': csize,
            'is_accepting_members': cis_accepting_members,
            'recruiting_cycle': crecruiting_cycle,
            'time_commitment': ctime_commitment
        }

        # Make sure there is input for all desired values
        if (not ctitle or not cdescription or not cmembership_process
                or not csize or not crecruiting_cycle or not ctime_commitment):
            flash("Please provide all inputs!")
            return render_template("/updateclub.html", club=updatedclub)
        
        # Updates club
        db_session.query(Club).filter_by(id=session["club_id"]).update(updatedclub)
        db_session.commit()

        flash("Club updated!")
        return redirect("/")


# Route for club deletion (post-only)
# POST: Delete club-related info from all tables
@bp.route("/deleteclub", methods=["POST"])
def deleteclub():
    
    # Removes clubs events from personal calenders
    db_session.execute("DELETE FROM calendars WHERE event_id IN (SELECT event_id FROM club_events WHERE club_id = :id)", {"id":session["club_id"]})

    # Removes club events from events from
    db_session.execute("DELETE FROM events WHERE id IN (SELECT event_id FROM club_events WHERE club_id = :id)", {"id":session["club_id"]})

    # Removes club leaders
    db_session.execute("DELETE FROM club_leaders WHERE club_id = :id", {"id":session["club_id"]})

    # Removes club events
    db_session.execute("DELETE FROM club_events WHERE club_id = :id", {"id":session["club_id"]})

    # Removes club tags
    db_session.execute("DELETE FROM club_tags WHERE club_id = :id", {"id":session["club_id"]})

    # Removes the club
    db_session.execute("DELETE FROM clubs WHERE id = :id", {"id":session["club_id"]})

    db_session.commit()

    flash("Club deleted!")
    return redirect("/")


# GET: displays club selection to decide which club's event to modify
# POST: sets club id and redirects to creation page
@bp.route("/createeventclub", methods=["GET", "POST"])
def createeventclub():

    # For testing purposes
    session["user_id"] = 1

    if request.method == "GET":
        
        # Gets all clubs [future TODO: change to get all clubs user leads]
        clubs = db_session.query(Club).all()

        # Makes sure user is a club leader (currently not necessary)
        if not clubs:
            flash("You Do Not Have Access To This Feature.")
            return redirect("/")

        return render_template("createeventclub.html", clubs=clubs)
    
    else:
        # Gets club id from dropdown
        club_id = int(request.form.get("process"))
        
        # If no club is selected, returns a prompt for user to select a club
        if not club_id:
            flash("Please Select A Club Before Submitting Form.")
            return redirect("/createventclub")

        session["club_id"] = club_id
        return redirect("/createevent")


# GET: renders blank creation page
# POST: gets form data, validates it, and insert event details into database
@bp.route("/createevent", methods=["GET", "POST"])
def createevent():

    # If page is loaded, renders survey for creating an event
    if request.method == "GET":
        newevent = Event(datetime = "", title = "", description = "")
        return render_template("createevent.html", event = newevent)

    # If form is submitted, get all the info and insert into events database
    else:
        
        # Gets title and description, adds them to newevent dict
        etitle = request.form.get("title")
        edescription = request.form.get("description")
        newevent = {
            'title': etitle,
            'description': edescription,
        }

        # Tries to convert datetime-local from form into datetime, otherwise reprompt for user input
        try:
            edatetime = datetime.strptime(request.form.get("datetime"), '%Y-%m-%dT%H:%M')
        except:
            try:
                newevent['datetime'] = datetime.strftime(request.form.get("datetime"),'%Y-%m-%dT%H:%M')
            except:
                pass
            flash("Please provide all inputs!")
            return render_template("updateevent.html", event=newevent)
        
        # [consideration TODO: make sure date is within certain bounds]
        newevent['datetime'] = edatetime

        # Ensure there is input for all desired values, otherwise reprompt for user input
        if (not etitle or not edescription):
            try:
                newevent['datetime'] = datetime.strftime(edatetime,'%Y-%m-%dT%H:%M')
            except:
                pass
            flash("Please provide all inputs!")
            return render_template("createevent.html", event = newevent)
        
        # All preconditions satisfied
        else:
            
            # Creates event object with given information, then adds to events table
            newevent = Event(
                title = etitle,
                description = edescription,
                datetime = edatetime
            )
            db_session.add(newevent)
            db_session.commit()

            # Adds club-event connection to club_events table
            newclubevent = ClubEvent(
                club_id = session["club_id"],
                event_id = newevent.id
            )
            db_session.add(newclubevent)
            db_session.commit()
            
            flash("Event added!")
            return redirect("/")


# GET: fetches club dropdown to select which club's event to modify
# POST: redirects to club-specific page to choose select which event to update
@bp.route("/selecteventclub", methods=["GET", "POST"])
def selecteventclub():

    # For testing purposes
    session["user_id"] = 1

    if request.method == "GET":

        # [future TODO: query clubs based on club leader status]
        clubs = db_session.query(Club).all()

        # Checks that user has clubs to modify
        if not clubs:
            flash("You Do Not Have Access To This Feature.")
            return redirect("/")

        return render_template("selecteventclub.html", clubs=clubs)

    else:
        
        # Retrieves club from dropdown, then redirects user to select their event
        club_id = int(request.form.get("process"))
        session["club_id"] = club_id
        return redirect("/selectevent")


# GET: displays events in a dropdown
# POST: saves event_id and moves to updateclub.html
@bp.route("/selectevent", methods=["GET", "POST"])
def selectevent():

    # For testing purposes
    session["user_id"] = 1

    if request.method == "GET":

        # Finds ids for every event by the given club
        event_idsdict = db_session.query().with_entities(ClubEvent.event_id).filter_by(club_id = session["club_id"])
        event_ids = []
        for item in event_idsdict:
            event_ids.append(item["event_id"])

        # Selects all club events, renders them in selectevent.html
        events = db_session.query(Event).filter(Event.id.in_(event_ids)).all()
        if not events:
            flash("You Do Not Have Access To This Feature.")
            return redirect("/")
        return render_template("selectevent.html", events=events)
    
    else: 
        event_id = int(request.form.get("process"))
        session["event_id"] = event_id
        return redirect("/updateevent")


# GET: renders form to update event
# POST: validates form and updates event
@bp.route("/updateevent", methods=["GET", "POST"])
def updateevent():

    if request.method == "GET":
        
        # Finds event info based on event_id, parses it, renders it as updateevent.html
        eventinfo = db_session.query(Event).filter_by(id = session["event_id"]).first()
        event = {
            'title': eventinfo.title,
            'description': eventinfo.title,
            'datetime': datetime.strftime(eventinfo.datetime, '%Y-%m-%dT%H:%M')
        }
        return render_template("updateevent.html", event=event)

    # If form is submitted, get all the info and insert into Event table
    else:
        
        # Gets title and description, adds them to newevent dict
        etitle = request.form.get("title")
        edescription = request.form.get("description")
        updatedevent = {
            'title': etitle,
            'description': edescription,
        }

        # Tries to convert datetime-local from form into datetime, otherwise reprompt for user input
        try:
            edatetime = datetime.strptime(request.form.get("datetime"), '%Y-%m-%dT%H:%M')
        except:
            try:
                updatedevent['datetime'] = datetime.strftime(request.form.get("datetime"),'%Y-%m-%dT%H:%M')
            except:
                pass
            flash("Please provide all inputs!")
            return render_template("updateevent.html", event=updatedevent)
        
        # [consideration TODO: make sure date is within certain bounds]
        updatedevent['datetime'] = edatetime

        # Ensure there is input for all desired values, otherwise reprompt for user input
        if (not etitle or not edescription):
            try:
                updatedevent['datetime'] = datetime.strftime(edatetime,'%Y-%m-%dT%H:%M')
            except:
                pass
            flash("Please provide all inputs!")
            return render_template("updateevent.html", event=updatedevent)
        
        # Updates event and commits update
        db_session.query(Event).filter_by(id=session["event_id"]).update(updatedevent)
        db_session.commit()
        flash("Event updated!")
        return redirect("/")


# POST: deletes event appearances in events and club_events
@bp.route("/deleteevent", methods=["POST"])
def deleteevent():
    db_session.execute("DELETE FROM club_events WHERE event_id = :event_id", {'event_id':session["event_id"]})
    db_session.execute("DELETE FROM events WHERE id = :event_id",{'event_id':session["event_id"]})
    db_session.commit()
    flash("Event deleted!")
    return redirect("/")