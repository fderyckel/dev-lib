from config import db
from typing import Dict, List, Any
from .models import Issues, Member


def check_errors(data: Dict[str, List]) -> bool:
    """Utility to check for errors in respones

    Args:
        response (Dict[str]): response from API

    Returns:
        bool: True if errors exist
    """
    if 'error' in data.keys():
        return True

    if len(data['message']) == 0:
        return True

    if len(data['message']) > 1:
        return data['message'][0]

    return


def check_availability(isbn: str) -> bool:
    """Checks the availability of the book if less than 10 members have
       Issued returns true else returns false

    Args:
        isbn (str): unique book identifier

    Returns:
        bool: True if book available false if not
    """
    issued = Issues.query.filter_by(isbn=isbn).all()

    if len(issued) > 10:
        return False
    return True


def issue_book(user_email: str, isbn: str,
               debt: int) -> bool:
    """Issues books if all conditions pass

    Args:
        user_email (str): user who is issuing
        isbn (str): book that the user is issuing
        debt (int): amount user owes

    Returns:
        bool: true if issue successful     
    """

    member = Member.query.filter_by(user_email=user_email).first()
    if member:
        """ User exists in the database
        """
        if member.debt > 500:
            return 'debt'
        issue = Issues(isbn=isbn, user=member.id, fee=debt)
        try:
            member.debt += debt
            db.session.add(member)
            db.session.add(issue)
            db.session.commit()
        except Exception as e:
            print(e)
            return False
        return True

    member = Member(user_email=user_email, debt=debt)
    try:
        db.session.add(member)
        db.session.commit()  # DO NOT REMOVE AS MEMBER.ID ONLY CREATED WHEN COMMITED
    except Exception as e:
        print(e)
        return False

    issue = Issues(isbn=isbn, user=member.id, fee=debt)

    try:
        db.session.add(issue)
    except Exception as e:
        print(e)
        return False

    db.session.commit()
    return True


def return_books(isbn: str, email: str) -> bool:
    """Remove issued book after performing validations

    Args:
        isbn (str): Unique Book ID
        email (str): Member Email

    Returns:
        bool: return True if record deleted
    """

    if member := Member.query.fiter_by(user_email=email):
        """ Member exists """
        issues = member.issue
        if issues:
            """ Has issued books"""
            for issue in issues:
                if issue.isbn == isbn:
                    db.session.delete(issue)
                    db.commit()
                    return True

        return False

    return
