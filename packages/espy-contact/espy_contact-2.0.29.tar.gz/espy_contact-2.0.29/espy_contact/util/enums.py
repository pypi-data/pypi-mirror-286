"""Copyright 2024 Everlasting Systems and Solutions LLC (www.myeverlasting.net).
All Rights Reserved.

No part of this software or any of its contents may be reproduced, copied, modified or adapted, without the prior written consent of the author, unless otherwise indicated for stand-alone materials.

For permission requests, write to the publisher at the email address below:
office@myeverlasting.net

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
import enum


class ResourceEnum(enum.Enum):
    POLL = "Poll"
    FORM = "Form"
    QUESTIONNAIRE = "QUESTIONNAIRE"
    TEXT = "Text"
    VIDEO = "Video"
    AUDIO = "AUDIO"
    FILE = "File"
    LINK = "Link"


class AccessRoleEnum(enum.Enum):
    ADMIN = "Admin"
    USER = "User"
    GUEST = "Guest"
    PARENT = "Parent"
    TEACHER = "Teacher"
    ACCOUNT = "Account"
    REFEREE = "Referee"
    STUDENT = "Student"
    STAFF = "Staff"

class SchoolTypeEnum(enum.Enum):
    ELEMENTARY = "Elementary"
    NURSERY = "Nursery"
    NURSERY_AND_PRIMARY = "Nursery and Primary"
    PRIMARY = "Primary"
    HIGHSCHOOL = "High School"
    POLYTECHNIC = "Polytechnic"
    UNIVERSITY = "University"
    POSTGRADUATE = "Postgraduate"


class GradeLevel(enum.Enum):
    PRESCHOOL = "PRESCHOOL"
    DAYCARE = "DAYCARE"
    KG1 = "Kindgergaten 1"
    KG2 = "Kindergaten 2"
    KG3 = "Kindgergaten 3"
    PRIMARY1 = "Primary 1"
    PRIMARY2 = "Primary 2"
    PRIMARY3 = "Primary 3"
    PRIMARY4 = "Primary 4"
    PRIMARY5 = "Primary 5"
    PRIMARY6 = "Primary 6"
    JSS1 = "Junior Secondary School 1 (JSS1)"
    JSS2 = "Junior Secondary School 2 (JSS2)"
    JSS3 = "Junior Secondary School 1 (JSS3)"
    SSS1 = "Senior Secondary School 1 (SSS1)"
    SSS2 = "Senior Secondary School 2 (SSS2)"
    SSS3 = "Senior Secondary School 3 (SSS3)"
    POST_UTME = "Post UTME (Post JAMB)"
    PREDEGREE = "Pre-degree"
    OND1 = "Ordinary National Diploma 1 (OND)"
    OND2 = "Ordinary National Diploma 2 (OND2)"
    HND1 = "Higher National Diploma 1 (HND1)"
    HND2 = "Higher National Diploma 2 (HND2)"
    YEAR1 = "One Hundred Level (University)"
    YEAR2 = "Two Hundred Level (University)"
    YEAR3 = "Three Hundred Level (University)"
    YEAR4 = "Four Hundred Level (University)"
    YEAR5 = "Five Hundred Level (University/Postgraduate)"
    YEAR6 = "Six Hundred Level (University/Postgraduate)"
    YEAR7 = "Seven Hundred Level (University/Postgraduate)"
    YEAR8 = "Eight Hundred Level (University/Postgraduate)"
    ONE = "ONE"
    TWO = "TWO"
    THREE = "THREE"
    FOUR = "FOUR"
    FIVE = "FIVE"
    SIX = "SIX"
    SEVEN = "SEVEN"
    EIGHT = "EIGHT"
    NINE = "NINE"
    TEN = "TEN"





class Term(enum.Enum):
    FIRST = "First"
    SECOND = "Second"
    THIRD = "Third"
    FOURTH = "Fourth"


class StatusEnum(enum.Enum):
    NEW = "New"
    ENROLLED = "Enrolled"
    ADMITTED = "Admitted"
    DEBTOR = "Debtor"
    DELETED = "Deleted"
    SUSPENDED = "Suspended"
    EXPELLED = "Expelled"
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"


class NigerianBank(enum.Enum):
    ACCESS_BANK = "Access Bank"
    CITIBANK = "Citibank"
    DIAMOND_BANK = "Diamond Bank"
    ECOBANK_NIGERIA = "Ecobank Nigeria"
    FIDELITY_BANK = "Fidelity Bank"
    FIRST_BANK_OF_NIGERIA = "First Bank of Nigeria"
    FIRST_CITY_MONUMENT_BANK = "First City Monument Bank"
    GUARANTY_TRUST_BANK = "Guaranty Trust Bank"
    HERITAGE_BANK_PLC = "Heritage Bank Plc"
    KEYSTONE_BANK_LIMITED = "Keystone Bank Limited"
    POLARIS_BANK = "Polaris Bank"
    PROVIDUS_BANK = "Providus Bank"
    STANBIC_IBTC_BANK = "Stanbic IBTC Bank"
    STANDARD_CHARTERED = "Standard Chartered"
    STERLING_BANK = "Sterling Bank"
    SUNTRUST_BANK_NIGERIA = "Suntrust Bank Nigeria"
    UNION_BANK_OF_NIGERIA = "Union Bank of Nigeria"
    UNITED_BANK_FOR_AFRICA = "United Bank for Africa"
    UNITY_BANK_PLC = "Unity Bank Plc"
    WEMA_BANK = "Wema Bank"
    ZENITH_BANK = "Zenith Bank"
class Appname(enum.Enum):
    aefinance= 'aefinance'
    essl='essl'
    harmonypflege='harmonypflege'
class GenderEnum(enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
class MonthEnum(enum.Enum):
    JANUARY = "January"
    FEBRUARY = "February"
    MARCH = "March"
    APRIL = "April"
    MAY = "May"
    JUNE = "June"
    JULY = "July"
    AUGUST = "August"
    SEPTEMBER = "September"
    OCTOBER = "October"
    NOVEMBER = "November"
    DECEMBER = "December"

