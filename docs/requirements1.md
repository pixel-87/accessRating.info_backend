So this is basically trip advisor or a similar website but for access rating.

# Requirements

## Database
### Fields
ID - Int(short), Autoincrement, (PK)

BusinessName - String

Address - String (regex on postcode?)

BusinessType - The type of business e.g. cafe, resturant, shop, pub.
+ specalisation - not required, a string added to the type e.g. italian resturant.

BusinessDescription - String (100 word limit?)
Would be editable by a business account. 

opening times?

Location - where pointer on map sits, there are two choices: lat and longitude, or what3words. What3words is easier for data entry imo. 

AccessibilityRating - The rating from 1 - 5 made by a volunteer, and then later approved by someone.

AccessibilityFeatures - Could be the specific note section, e.g. go to side window and ask for ramp, would be shown next to rating when clicked into further.
This would be editable by the business as a business account

ContactInfo - business contact info, taking either email or phone number.

FirstAssessedDate - Date the business was first assessed.

NextAssessmentDate - The date of the next assessment. (could be automatic or could be scheduled)

AccessReport - The full report of how accessible it is, would be provided alongside the `AccessabilityRating` and `AccessabilityFeatures` for users wanting more info. 

Ratings - Ebay-style reviews of positive, neutral, negative. 
Users can add the following:
- Rating - positive, neutral, or negative (required if users adds others).
- Comment - Users can leave a comment of their experience.
- Photo - Photos.

## Accounts
Need a business account for businesses to adjust data about their business, to request re-assessments, to request stickers (two types of stickers, sticky on image, sticky on back.)

Users need an account to store favourites, leave reviews.

superuser/admin for adding businesses.

## Stickers
5 different stickers for the different ratings (graphic/colours), 
qr code gen based on name of business and/or ID number
