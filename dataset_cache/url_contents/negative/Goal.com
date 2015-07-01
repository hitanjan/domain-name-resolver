About Goals - Analytics Help         CalendarTranslateMobileBooksWalletShoppingBloggerFinancePhotosVideosDocsEven more »Account Options   Analytics Help     Please fill out this brief survey to help us improve the Analytics Help Center.     About Goals Use Goals to measure how often users complete specific actions.  Goals measure how well your site or app fulfills your target objectives. A Goal represents a completed activity, called a conversion, that contributes to the success of your business. Examples of Goals include making a purchase (for an ecommerce site), completing a game level (for a mobile gaming app), or submitting a contact information form (for a marketing or lead generation site).
Defining Goals is a fundamental component of any digital analytics measurement plan. Having properly configured Goals allows Google Analytics to provide you with critical information, such as the number of conversions and the conversion rate for your site or app. Without this information, it's almost impossible to evaluate the effectiveness of your online business and marketing campaigns.
Watch the video below for an overview of Google Analytics Goals.

In this article:


How Goals work
Goal types
Funnels for Destination Goals
Goal value
Goal ID and Goal sets
Reporting on Goals
Limits of Goals
Best practices for Goals
Next steps


How Goals work
Goals are configured at the view level. Goals can be applied to specific pages or screens your users visit, how many pages/screens they view in a session, how long they stay on your site or app, and the events they trigger while they are there. Every Goal can have a monetary value, so you can see how much that conversion is worth to your business. Using values for Goals lets you focus on the highest value conversions, such as transactions with a minimum purchase amount.
When a visitor to your site or user of your app performs an action defined as a Goal, Google Analytics records that as a conversion. That conversion data is then made available in a number of special-purpose reports, which are described below.
Goal types
Goals fall into one of 5 types, listed in the table below:



Goal Type
Description
Example


Destination
A specific location loads
Thank you for registering! web page or app screen


Duration
Sessions that lasts a specific amount of time or longer
10 minutes or longer spent on a support site


Pages/Screens per session
A user views a specific number of pages or screens
5 pages or screens have been loaded


Event
An action defined as an Event is triggered
Social recommendation, video play, ad click



Funnels for Destination Goals
With a Destination Goal, you can specify the path you expect traffic to take. This path is called a funnel. When you specify steps in a funnel, Analytics can record where users enter and exit the path on the way towards your Goal. This data appears in the Goal Flow and Funnel reports. You may see, for example, a page or screen in a funnel from which a lot of traffic exits before completing the Goal, indicating a problem with that step. You might also see a lot of traffic skipping steps, indicating the path to conversion is too long or contains extraneous steps.
Learn more about Goal Flow and Funnel reports.

Goal value
When you set up a Goal, you have the option of assigning a monetary amount to the conversion. Each time the Goal is completed by a user, this amount is recorded and then added together and seen in your reports as the Goal Value.
Every action a user takes can be translated into a dollar amount. One way to help determine what a Goal value should be is to evaluate how often the users who complete the Goal become customers. For example, if your sales team can close 10% of people who sign up for a newsletter, and your average transaction is $500, you might assign $50 (i.e. 10% of $500) to your newsletter sign-up Goal—a Goal that users complete when they reach the final newsletter sign-up page. In contrast, if only 1% of signups result in a sale, you might only assign $5 to your newsletter sign-up Goal.

You can change the currency unit for the Goal Value in your view settings.

Goal ID and Goal sets
Every Goal you create is assigned a numeric ID, from 1 to 20. Goals are grouped into sets of up to 5 individual Goals. Goal sets allow you to categorize the different types of Goals for your site. For example, you might track downloads, registrations, and receipt pages in separate Goal sets. These sets appear in your reports as links beneath the Explorer tab in many reports.
The Analytics blog post from June 14, 2012 has a great example of how to organize Goal sets.
Reporting on Goals
You can analyze the Goal completion rates, or conversion rates, in the Conversion > Goals reports. Goal conversions also appear in other reports, including the Conversions > Multi Channel Funnels reports, the Conversions > Attribution reports, and the Acquisition reports.
Limits of Goals
Goals are limited to 20 per reporting view. To track more than 20 Goals, create an additional view for that property, or edit an existing Goal you don't need anymore.
Goals apply to the data you collect after the Goal has been created. In other words, you must set up Goals in your Google Analytics account before data appears in your Goal reports and any other report that provide data on Goals and Goal Conversions.
Goals can't be deleted, but you can stop recording data for a Goal. 
Best practices for Goals
Use intuitive names for your Goals. This will help you and others understand the conversion reports more easily.
Although assigning a Goal value is optional, we recommend you do so to help monetize and evaluate your conversions. Note that Google Analytics also uses the Goal value data to calculate other metrics like ROAS (Return on Ad Spend). If using a dollar amount as a Goal value doesn't seem applicable to your site or app, just use a consistent numeric scale to weight and compare your conversions. For example, give low-value Goals a "1" and high-value Goals a "10."
If you change or repurpose an existing Goal, be sure to keep track of when you made the change. Since Goals are not applied to historical data, changing a Goal will change your conversion data from the point of the change. This might lead to confusion in your reports. (This is another reason to name your Goals intuitively).
Next steps
Set up and edit Goals.
See Goal examples and use cases.
Learn more about the Goal Flow report.
Troubleshoot Goal issues.
                 How helpful is this article:Feedback recorded. Thanks!Not at all helpfulNot very helpfulSomewhat helpfulVery helpfulExtremely helpful   Create and manage GoalsAbout GoalsCreate, edit, and share Goals     ©2015 Google   Privacy Policy   Terms of Service     Bahasa Indonesia‎català‎dansk‎Deutsch‎English‎español‎Filipino‎français‎hrvatski‎italiano‎latviešu‎lietuvių‎magyar‎Nederlands‎norsk‎polski‎português‎português (Brasil)‎română‎slovenčina‎slovenščina‎suomi‎svenska‎Tiếng Việt‎Türkçe‎čeština‎Ελληνικά‎български‎русский‎српски‎українська‎עברית‏العربية‏हिन्दी‎ไทย‎中文（简体）‎中文（繁體）‎日本語‎한국어‎                