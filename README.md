# Capella

## Installation

`pip install Capella`

### To Run:
Navigate to your python installation and go to `lib\site-packages` open the `Capella` directory in your terminal and run `main.py`, the GUI will open from the terminal.

---

### Introduction

Capella is a simple-to-use Astronavigation aid. The program will derive a celestial position from a minimum of inputs and plot the position on a chartlet, with an analysis of the accuracy of  computed position provided. The program  additionally features some helper functions for celestial observation session planning, DR computation and compass correction. 


![](gifs/demo.gif)

---
## Section 1: Sight Entry

**DR Information**

All effective navigation starts with keeping a DR. Capella is no different. For the program to work effectively, first provide a DR position, time, course and speed. 

Capella uses the standard nautical conventions for time and position formatting, and all times are kept in UTC. Capella will format the input for you---just type in the numbers for the respective field and when you are finished press tab or click to advance to the next input field. If erroneous information has been inputted, the field will flag RED. 


**Sight Entry**

In the Step 2 section, complete the four required fields. All the input fields will assist with autocompletion and formatting. The fields are: 1. Body 2. Hs Value 3. Sight Date 4. Sight Time. 
All sextant altitude corrections are handled internally, simply input the Hs value for the observation.

When you have completed the four input fields, hit the *Add* button and the sight will appear in the Sight List at the top of the screen. To edit previously entered information, click on the sight in the *Sight List*, the sight's information will populate the sight entry fields under Step 2. Make any required changes and hit *Update* and the sight entry will change in the *Sight List*. To remove a sight from the *Sight List*, simply click on the sight and hit *Delete*. Multiple sight handling is easily achieved using the conventional Shift or Ctrl + click features. 


*Averaging*

If you have multiple observations of the same body, you can CTRL or SHIFT click on them in the Sight Entry area, and the average of their Hs and time/date values will appear in the Step 2-Entry area. Press the *Add* button to add the averaged sight. It is recommended you first compute the position with all sights unaveraged and use the *Fit-Slope Analysis* feature to find which values should be eschewed or kept for averaging.

![](gifs/blunder_3.png)

*LOP plot before fit-slope analysis and sight averaging*

![](gifs/blunder_fixed.png)

*LOP plot after fit-slope analysis and sight averaging*

*Almanac Computation*

Capella features a high-accuracy perpetual almanac valid from the years 1900-2050, with the data taken from the JPL de421 database. Once the fix is computed, all almanac data is displayed in the *Sight Data/Planning* section. 

**Fix Computation**

Capella will calculate a fix from the DR information provided in Step 1 and the sights added to the Sight List. A fix can be calculated from just one sight and the provided DR information, however the algorithm needs at least 2 sights to provide a more accurate fix. Once two or more sights are present in the *Sight List* and a *Fix Time* and *Fix Date* has been provided in the *Step 1* field, hit the *Compute* button or press *CTRL-l*. Capella will calculate a running fix based on the DR and *Fix Time* information provided. The calculated results as well as a DR position for the requested *Fix Time* will appear highlighted at the bottom. 

A position is calculated using a Limited Memory-BFGS algorithm. The algorithm is robust with respect to erroneous DR information, and can effectively handle high altitude sights. Prudent navigation always requires the most accurate DR possible, however, the fitting algorithm is quite robust with respect to DR accuracy. 

*Example 1:*

The Sight Information below yields the fix: **40-14.0-N, 049-58.0-W**.
```
| DR Date   | DR Time  | DR L      | DR λ       | Course | Speed | I.C. | H.O.E | Temp. | Press. | Fix Date  | Fix Time |
| --------- | -------- | --------- | ---------- | ------ | ----- | ---- | ----- | ----- | ------ | --------- | -------- |
| 1993-5-13 | 07:30:00 | 40-10.0-N | 050-15.0-W | 090    | 5.5   | -1.2 | 7     | 10    | 1010   | 1993-5-13 | 07:44:00 |

| Body       | Hs      | Date       | Time     |
| ---------- | ------- | ---------- | -------- |
| Kochab     | 43-23.8 | 1993-05-13 | 07:33:45 |
| Rasalhague | 51-05.2 | 1993-05-13 | 07:35:16 |
| Alkaid     | 30-15.9 | 1993-05-13 | 07:37:15 |
| Altair     | 58-38.0 | 1993-05-13 | 07:39:02 |
| Venus      | 15-15.3 | 1993-05-13 | 07:41:24 |
| MoonLL     | 34-05.6 | 1993-05-13 | 07:44:08 |
```
by changing the DR Position to 00-00.0-N and 000-00.0-W *--a position 3673 nm away--* and keeping the same observation data, Capella yields the fix: **40-14.3-N, 049-57.8-W**. 

**Systematic Error**

If Capella's systematic error algorithm detects uncorrected index and personal error, a prompt will appear asking you could like to remove the error from your observations and recompute the fix. Click *Ok* and then click *Compute*. This process can be iterative and the prompt might appear multiple times, with each cycle bringing the calculated fix closer to the observer's true position. This method isn't a magic bullet, but can yield impressive results in certain circumstances. 


**Loading and Saving Observation Records**

Capella uses the computer's clipboard as a means of loading and saving observations. Rather than saving the observations in a proprietary format, the observations are copied to the clipboard as a simple markdown format table than can be pasted into any .txt file the navigator wishes to use as a sight log. 

*To Save Sights*
1. In Capella, click File-Save Sights to Clipboard or CTRL-s. 
2. 2 markdown format tables will be saved to your computer's clipboard.
3. Paste them in any .txt file you would like to use as a log. 

*To Load Sights*
1. Highlight the 2 tables that you pasted into the .txt file of choice. 
2. Copy to the computer's clipboard via CTRL-C or using the mouse.
3. In Capella, click File-Load Sights from Clipboard or CTRL-l

*Why do it like this?*
1. Simplicity. You can use one E-log for record keeping, note taking and to interact with the program. 
2. Using the "Windows-Snap" features on a computer allows you to snap Capella to one side of the screen and snap the `.txt` sight log of choice to the other. Using the `ctrl` quick keys you can rapidly edit the observations in the `.txt` log and compute the observations in Capella side by side. 
3. Most celestial navigation programs have UI issues that are difficult and frustrating to navigate, using this method, you can use any text editor as the primary controller of the program if you'd like. Simply use the below template:
```
| DR Date    | DR Time   | DR L      | DR λ       |   Course |   Speed |   I.C. |   H.O.E |   Temp. |   Press. | Fix Date   | Fix Time   |
|------------|-----------|-----------|------------|----------|---------|--------|---------|---------|----------|------------|------------|
| 2012-07-06 | 12:30:00  | 47-25.9-N | 007-08.0-W |      208 |      17 |    0.4 |      86 |      10 |     1010 | 2012-07-06 | 12:33:22   |
 
| Body   | Hs      | Date       | Time     |
|--------|---------|------------|----------|
| SunLL  | 65-03.4 | 2012-07-06 | 12:29:22 |
```

![](gifs/saving_loading.gif)

---


## Section 2: LOP Plot

**Exploring the plot**

Once the fix is computed from the *Sight Entry* page, the LOP's for the observations are automatically plotted. The plot is highly customizable with respect to  size, aspect and zoom via the buttons located in the lower right corner. Click the *NSEW arrow* icon and then left-click and drag on the plot to move the plot, the Latitude and Longitude scales will automatically change. A right-click and drag will change the plots aspect. To reset the plot back to the default at any time, click on the *House* icon. To zoom in on the plot, click the *Magnifying Glass* icon and then left-click and drag to zoom-in and right-click and drag to zoom-out. 

Wherever the mouse travels in the plot area, the Lat/Long position will appear in the lower right corner. To save the plot as a PNG image, select the *Floppy Disk* image in the lower right corner.

**Plot Information**

The LOPS are automatically advanced with the course and speed information provided in the *Sight Entry* section and bodies are labeled on the plot and in the sight key area. Additionally, the computed DR position for the *Fix Time* is also plotted. If the DR is very far from the LOP plot, the plot will need to be zoomed for a better aspect, however, if a good DR is being kept, this should not be necessary in most cases. 

**Fix + Confidence**

The red dot on the LOP plot marks the computed position and the golden ellipse surrounding the computed fix represents an area of 95% confidence. That is, there is a 95% probability, *given the sight information provided* that the true position lies within the ellipse.

![](gifs/confidence_ellipse.png)

---
## Section 3: Fit Slope Analysis

This is an implementation of Dr. David Burch's Fit Slope method. It is a means of deriving greater accuracy from our sight observations and attempting to spot any outliers or potential blunders. 

**How  Fit-Slope Analysis works**

The vessel is moving all the time at sea and and the celestial objects are moving all the time as well. If we take 3 observations of the Sun, how do we know which observations were accurate and which weren't? 

A simple averaging of the sights and times may not yield more accurate results if one of the observations is erroneous--However, the ascending or descending slope of the body can be computed and plotted as a function of time and estimated position, and the slope will be mostly linear as long as the timescale is fairly short.

We can then plot our observation relative to this sloping line. If our observation is way off of the slope, the sight is likely a blunder, if it is close to the slope it was likely O.K. With multiple observations this allows us to find any outliers. Using the 3 Sun observation example, if 2 observations scatter close to the fitted slope and another scatters way off of the slope, we know we can discard that observation as it was likely a blunder. If All three observations scatter within 1 or 2 arc minutes of the fitted slope, we can safely average the sights to reduce the amount of error in our observations. 

**Plot Information**
 
Each plot on the *Fit-Slope* page has a fitted *slope* and a *red dot*. The *slope* represents the computed altitude at the DR Position one minute behind the DR position of the observation and the computed altitude at the DR position one minute ahead of the DR position of the observation. A red dot is the observed altitude at the time of the observation. With this information you can see if your observation was under-observed or over-observed. the *Scatter* value at the top of each plot tells you how by how many minutes of arc your observation was over or under the computed slope.  The X-axis scale is minutes after the hour of observation, and covers a 2 minute timescale. The Y-axis scale is the computed range of altitudes for the observed body over that 2 minute scale. As with the LOP Plot page, every plot is fully interactive and explorable using the buttons in the lower left corner, and the values for any point on the plot will appear in the lower right corner.

*Example 2:*

The following observations are taken and a fix of 21-11.0-N, 157-34.7-W is computed, the observer's actual position is: 21-12.0-N, 157-30.0-W. 
```
| DR Date    | DR Time   | DR L      | DR λ       |   Course |   Speed |   I.C. |   H.O.E |   Temp. |   Press. | Fix Date   | Fix Time   |
|------------|-----------|-----------|------------|----------|---------|--------|---------|---------|----------|------------|------------|
| 1990-01-02 | 03:00:00  | 21-12.0-N | 157-30.0-W |        0 |       0 |      0 |       0 |      10 |     1010 | 1990-01-02 | 03:12:00   |

| Body      | Hs      | Date       | Time     |
| --------- | ------- | ---------- | -------- |
| Deneb     | 50-15.0 | 1990-01-02 | 03:00:00 |
| Fomalhaut | 38-54.0 | 1990-01-02 | 03:01:00 |
| Aldebaran | 15-32.0 | 1990-01-02 | 03:02:00 |
| Deneb     | 49-27.0 | 1990-01-02 | 03:05:00 |
| Fomalhaut | 38-46.0 | 1990-01-02 | 03:06:00 |
| Aldebaran | 16-30.0 | 1990-01-02 | 03:07:00 |
| Deneb     | 48-38.0 | 1990-01-02 | 03:10:00 |
| Fomalhaut | 38-37.0 | 1990-01-02 | 03:11:00 |
| Aldebaran | 17-50.0 | 1990-01-02 | 03:12:00 |
```

The fit slope analysis shows that the Aldebaran observation at 03:07:00 scatters 9.79 arc minutes under the computed slope while the other Aldebaran observations are + 0.64' and + 1.74' respectively. This observation is clearly a blunder, and the LOP plot confirms that it is far away from our other LOPS so it is removed altogether from the *Sight List* and a new position is computed: 
21-12.0-N, 157-31.5-W. The position can be further refined, by either selecting the individual sights with the least scatter, or averaging each set since the Fit-Slope analysis confirms their normal distribution, both methods will yield a fix with a similar level of accuracy. 

![](gifs/blunder.png)

*Capella screens for potentially erroneous shots using statistical tests and will alert the user to a potential blunder*

![](gifs/blunder_2.png)

*A fit slope analysis of a sight session, we see that of the two Aldebaran observations, one scatters far off of the correct slope and is likely a blunder*

---

## Section 4: Planning/Session Data


**Sight Planning** 

The *Sight Planning* utility provides a quick and convenient means of plotting a round of observations prior to a sight session. Enter a UTC date and time in the provided sight fields and then hit the *Set Time* button. Using the provided DR date/time, Lat/Long and course/speed in the *Sight Entry* page, a DR position for the selected time and will appear in the two fields below. The *Time of Phenomena*, *Body List* and *Optimal Triads* will now be populated with information. 

*Time of Phenomena*

A list of major celestial phenomena for a 24 hour period is displayed. All the times are corrected with a "second estimate" based on the DR information provided.

*Body List*

A list of all celestial bodies that are visible at the specified time and computed DR position that are between 25 and 65 degrees in altitude. Their altitude, azimuth and magnitude are calculated for the specified time and calculated DR position and listed in a scrollable table. 

*Optimal Triads*

A weighting algorithm will list optimal groupings of 3 celestial objects based on azimuthal distribution, magnitude and altitude and list them in a scrollable table.

*Example 3:*

it is 2012-07-06 at 09:00:00 UTC and we wish to plan for the day's observations. We input the below information in the *Sight Entry* DR fields. 
```
| DR Date    | DR Time  | DR L      | DR λ       | Course | Speed | I.C. | H.O.E | Temp. | Press. |
| ---------- | -------- | --------- | ---------- | ------ | ----- | ---- | ----- | ----- | ------ | 
| 2012-07-06 | 09:00:00 | 48-18.4-N | 006-26.5-W | 208    | 17    | 0.4  | 86    | 10    | 1010   | 
```

We enter the 2012-07-06, 09:00:00 UTC in the input fields in the Planning Controls tab and hit *Set Time*. We click on the time of phenomena tab and see that L.A.N. will occur at 12:33:21 UTC. and PM Nautical Twilight will be around 21:00:00 UTC. 

At 12:30:00 UTC we begin a round of noon sights:
```
| DR Date    | DR Time   | DR L      | DR λ       |   Course |   Speed |   I.C. |   H.O.E |   Temp. |   Press. | Fix Date   | Fix Time   |
|------------|-----------|-----------|------------|----------|---------|--------|---------|---------|----------|------------|------------|
| 2012-07-06 | 12:30:00  | 47-25.9-N | 007-08.0-W |      208 |      17 |    0.4 |      86 |      10 |     1010 | 2012-07-06 | 12:33:22   |
 
| Body   | Hs      | Date       | Time     |
|--------|---------|------------|----------|
| SunLL  | 65-03.4 | 2012-07-06 | 12:29:22 |
| SunLL  | 65-05.3 | 2012-07-06 | 12:33:22 |
| SunLL  | 65-05.4 | 2012-07-06 | 12:34:22 |
| SunLL  | 65-05.6 | 2012-07-06 | 12:35:22 |
| SunLL  | 65-05.6 | 2012-07-06 | 12:36:22 |
| SunLL  | 65-05.6 | 2012-07-06 | 12:37:22 |
| SunLL  | 65-05.4 | 2012-07-06 | 12:38:22 |
```
The *Fit Slope Analysis* tab confirms that our 12:33:22 observation was the meridian transit, agreeing with the computed 12:33:21 estimate. Our 12:33:00 computed Latitude at LAN is therefore 47-24.7- N, and the GHA of our LAN observation is 007-08.1 - this is listed in the *Sight Data* table. Our computed position is therefore 47-24.7-N, 007-08.1-W. 

We enter our fix as our new DR on the *Sight Entry* page and enter 21:00:00 UTC - the approximate time of Nautical Twilight we computed earlier - in the time field under *Planning Controls*. Our 21:00:00 UTC DR position updates to 45-18.3-N, 008-46.0-W. Under *Body List* we see all of the optimal bodies to shoot for 21:00:00 UTC Star Time, calculated for DR position 45-18.3-N, 008-46.0-W. Under *Optimal Triads* we see the best 3-body groupings listed in order, weighted by azimuthal distribution, altitude and magnitude. 

Our plan is preset our sextant with the below listed values and try to get at least 3 observations of each body, weather permitting. 

*Optimal Triad 1*

| Body          | Alt     | Az  | Mag  |
| ------------- | ------- | --- | ---- |
| Alioth        | 64-10.1 | 308 | 1.76 |
| Zubenelgenubi | 28-06.5 | 189 | 2.75 |
| Deneb         | 36-51.7 | 60  | 1.25 |

**Sight Data**

The *Sight Data* table lists relevant almanac and observation data for the sights that were used for the sight reduction process. Capella DR's automatically using the time of each sight and the listed Session DR time and position in order to compute the Alt, Az and Intercept values. These values are not used in the automatic plotting process, but can be used if the navigator wishes to use a paper plot. 'Best Sights'  with the lowest scatter from the *Fit Slope Analysis* are highlighted in green for easy identification.

**Analytics**

*Best Sights*

A list of the observations with the lowest scatter values per body. If only one body is observed but at distinct times, then the 'best' value is computed for each block of time. For example, in the below example the 'best' values are computed for 3 distinct blocks of time, the 1993-07-07 21:00:00 and 23:00:00 sessions and the 1993-07-08, 00:30:00 session. 
```
| DR Date   | DR Time   | DR L    | DR λ     |   Course |   Speed |   I.C. |   H.O.E |   Temp. |   Press. | Fix Date   | Fix Time   |
|-----------|-----------|---------|----------|----------|---------|--------|---------|---------|----------|------------|------------|
| 1993-7-7  | 15:21:00  | 39-46-N | 161-20-W |      265 |       6 |   -1.5 |       9 |      10 |     1010 | 1993-7-8   | 00:33:12   |
 
| Body  | Hs      | Date     | Time     |
| ----- | ------- | -------- | -------- |
| SunLL | 65-04.7 | 1993-7-7 | 21:30:17 |
| SunLL | 65-19.7 | 1993-7-7 | 21:31:55 |
| SunLL | 72-23.8 | 1993-7-7 | 23:02:04 |
| SunLL | 72-19.4 | 1993-7-7 | 23:03:49 |
| SunLL | 63-00.2 | 1993-7-8 | 00:31:28 |
| SunLL | 62-44.9 | 1993-7-8 | 00:33:12 |
```
In a case where all of the bodies are distinct, they are all their own 'best' and every sight will be listed under *Best Sights*  and will be highlighted green in the *Sight Data* field. 

*Position Errors*

A table with the one and two Sigma errors for the fitting algorithm converted into nautical mile estimates. The goal is to provide the navigator with an estimate as to where their celestial fix has placed them vs. where they might actually be. However, It is important to remember that these errors are only relevant to the fit of the *information provided* and are not a magic bullet. For example, a two body fix is by definition an *exact* position, X marks the spot so to speak, and the 95% error estimate will be close to zero, however(!), the *exact* position is likely not *exactly* where you are. 

Celestial Navigation under the most optimal and rigorous circumstances can provide a positional accuracy of around 1 nm, it is not a GPS. As always the prudent navigator uses more than one means of position fixing to navigate.

---

## Section 5: Azimuth


**Observation Input**

In the *Observation Input* section, fill in the required input fields with the body observed, the gyro bearing and time and position of the observation. As with all other fields of their type in the program, autocompletion and format checking are provided to assist the navigator. 

The output is provided in the *Compass Observations Records* field in the exact format used in the usual *Compass Observation Book* required by IMO standards. The Gyro Error, Compass Error, and Magnetic Variation and Magnetic Deviation are calculated. Magnetic Variation can be calculated for any position in the world and uses the World Magnetic Model Epoch 2020. The list of gaussian coefficients is internal to the program and is valid through 2025. 

--- 

# A short, true, sea story (An end-to-end example of usage)

We're on a large commercial vessel steaming from the Pacific Northwest to Hawaii at a speed of 12 kts on a course of 251 True. It's 19:55 ship's time, the third mate is back on the bridge, and we've been relieved of the watch. The third mate pours a cup of coffee and jokes that the sun has just set and star time is upon us. "Show off your fancy program!" he says. "Sure!", we say. We grab the ship's sextant from under the chart table and fire up *Capella*.

We enter our DR information, using 05:00:00 UTC as our DR time and choose DR coordinates we know we are within 100 NM of. We're  being deliberately vague. We know our height of eye to within 30 feet so we guess that its 158 feet. It's a big ship. 

We proceed to the sight planning section and enter 05:15:00 as the time we'd like to generate sights for. We won't preset our sextant, we just want a general orientation of the evening's sky. We note the brightest and most visible stars and planets, quickly scratch them down, and then grab the sextant and head out on the bridge wing.  

Once outside we find the sky is largely overcast. A quick shot of the horizon suggests the index error is around 2.0' on the arc. We look up and scan the sky. Sirius pops through the clouds and we grab 3 quick sights in succession. About 10 minutes later Rigel briefly shows up in between the clouds and we're able to grab 2 quick sights. Capella briefly emerges and we're able to get one shot, but then the clouds shroud the star and it remains hidden. Discouraged, we grab 2 quick lower limb shots of the moon and head back to the chart room. The shots were fast and likely not very precise, we don't expect much. The third mate is amused at our obvious frustration.

We write everything down and look over the shots:

```
| Body    | Hs      | Date       | Time     |
| ------- | ------- | ---------- | -------- |
| Sirius  | 51-13.8 | 2022-03-18 | 05:04:06 |
| Sirius  | 51-12.2 | 2022-03-18 | 05:05:44 |
| Sirius  | 51-22.1 | 2022-03-18 | 05:07:16 |
| Rigel   | 54-15.2 | 2022-03-18 | 05:15:48 |
| Rigel   | 54-21.5 | 2022-03-18 | 05:17:16 |
| Capella | 61-34.0 | 2022-03-18 | 05:13:42 |
| MoonLL  | 11-30.5 | 2022-03-18 | 05:18:57 |
| MoonLL  | 11-45.6 | 2022-03-18 | 05:20:25 |
```

We enter all of our sights and  calculate a fix using all of the observations. Immediately, *Capella* prompts us with a message box saying that something is likely wrong with our 05:17:16 Rigel observation. We look at the LOP plot and notice that it is an obvious blunder. 

We remove the Rigel shot and re-compute the fix. We are now greeted with a message box saying that there is systematic error in our observations and are asked if we would like to recompute. We decided to first use the fit-slope analysis tool to see if any one shot is adding extra weight to the error calculation. 

The fit-slope plots show that 2 of our Sirius shots scatter above the fitted line, while the middle observation scatters below. An analysis of the LOP's also suggests that our middle Sirius shot is a potential outlier. We remove the second Sirius observation and average the rest of the sights. We again calculate our position and are again greeted with a message box asking us to remove systematic error. It's clear we've overestimated our height of eye or incorrectly deduced our index error, so we click yes and remove the error and recompute our position again and receive no more messages. 

The fix was calculated for 05:18:00 and we get the following prediction: 21-51.5 N, 155-41.0 W. We go back to the LOP plot section and note a nice tight cocked hat and small confidence ellipse -- with a small amount of logical deduction we've turned a fairly messy fix into what looks like a pretty good one. We note the ship's GPS log and see that our 05:18:00 UTC position was 21-51.2, 155-41.4, *we were only .55 NM off*. Pleased, we wink at the third mate, put the sextant back in the box and stroll off of the bridge, only to hurry down the ladderwell to our stateroom--*we have to be back on watch in 5 hours*.

### Above Steps Demonstrated

![](gifs/poa_shots.gif)

---
#### Disclaimer:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

### About

Capt. Alex Spradling holds 1600 Ton Master Oceans, and 2nd Mate Unlimited Tonnage Oceans Licenses and actively sails as a deck officer in the U.S. Merchant Marine. He is a graduate of SUNY Maritime College. 
