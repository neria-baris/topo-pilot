# סקירת ספרות: שלושה כיוונים להמשך

תאריך: 2026-11-04. מסמך זה נשען על מפת הספרות הקודמת של הפרויקט (`docs/proposals/RESEARCH_LANDSCAPE.md`, 2026-10-13), שבה המקורות כבר נבדקו מול הרשומות הראשיות. כאן לא חוזרים עליה. הסקירה מוסיפה את מה שחסר בה: הוויכוח על הופעת תאי רשת ותאי כיוון ראש, השוואת ארכיטקטורות על משימות סינון, משטחים לא־אוריינטביליים, קודי אוכלוסייה הסתברותיים, ועבודות חדשות שנוגעות בשלושת הכיוונים.

## 1. תקציר

ידוע היטב שמודלים שמאומנים לנבא את הסמל הבא בונים בתוכם ייצוג של "האמונה", כלומר ההתפלגות המלאה על המצב הנסתר. ייצוג זה ליניארי ברובו, נמצא במודלים קטנים ובמודלי שפה גדולים, וניתן להתערב בו. ידוע גם שמושגים מחזוריים (ימי השבוע, חשבון מודולרי) מיוצגים על מעגלים, ושמודלים שמאומנים לניווט מפתחים לפעמים קודים מרחביים. אבל הופעת הקודים האלה תלויה מאוד בבחירות האימון. יש כבר עבודות קרובות מאוד לפרויקט. ברנר ושותפיו (2026) מראים שגאומטריית הניבוי מעצבת ייצוגים של הולך על סריג. ג'רפליה (2026) מראה שמשתנה נסתר מחזורי שנשתל בנתונים מוליד גאומטריה של טבעת. לכן "מופיע מעגל" אינו חידוש כשלעצמו. הפערים הברורים הם שלושה. (א) אף עבודה שמצאנו לא בדקה אילו *סטטיסטיקות* של אמונה על מעגל המודל שומר: זווית בלבד, או גם ריכוז, ובאיזו צורה. במדעי המוח יש לכך מודל מוכן, הטבעת הבייסיאנית שבה גובה הבליטה מקודד ודאות, אבל ברשתות מלאכותיות על עולם עם אמת מדויקת זה לא נבדק. (ב) השוואה שיטתית של ארכיטקטורות ופונקציות הפסד מול אורקל מדויק קיימת רק חלקית. (ג) משטחים לא־אוריינטביליים כעולם נסתר של מודל רצפים כמעט לא נחקרו. הניסיון שלנו עצמנו מראה שהמשימה קשה ללמידה.

## 2. לפי נושא

### 2.1 גאומטריית אמונה במודלי רצפים
**מה ידוע:** הזרם השיורי של טרנספורמר מייצג ליניארית את סימפלקס האמונות של התהליך הנסתר, גם כשהגאומטריה פרקטלית. עבודות המשך מסבירות את הגאומטריה כעדכון אמונה מוגבל על ידי הארכיטקטורה, מראות שגם רשתות חוזרות לומדות זאת, ומראות שמודלי שפה גדולים בונים גאומטריה כזו בתוך ההקשר.
- Shai et al. 2024, NeurIPS: אמונות ליניאריות בזרם השיורי.
- Piotrowski, Riechers, Filan & Shai 2025, ICML: עדכון אמונה מוגבל.
- Riechers, Elliott & Shai 2025: טרנספורמרים ו־RNN לומדים אמונות על מודלים "קוונטיים" ו"פוסט־קוונטיים".
- מהמפה הקודמת: Shai et al. 2026 (ייצוגים מפורקים לגורמים), Balcells et al. 2026 (אמונות בהקשר במודלי שפה, כולל התערבות), Sarfati et al. 2026 (יריעות של התפלגויות פוסטריוריות), Brenner, Knösche & Scherf 2026, Jerpelea 2026.
- Agarwal, Dalal & Misra 2025: טענה לפוסטריורים בייסיאניים מדויקים בקשב. בניסוי שלהם, על משימת מודל מרקוב נסתר, LSTM קורס לממד אחד ו־Mamba שומר מבנה מבוזר.

**מה זה אומר לנו:** המסגרת הכללית ("המודל מייצג את האמונה") תפוסה. התרומה שלנו צריכה להיות על **הטופולוגיה** של משתנה האמונה ועל **הסטטיסטיקה המצומצמת** שהמודל שומר.

### 2.2 מאפיינים מעגליים ומחזוריים
**מה ידוע:** במודלי שפה יש מאפיינים רב־ממדיים מעגליים, והמודל משתמש בהם לחשבון מחזורי. ברשתות לחשבון מודולרי נמצאו שני אלגוריתמים שונים, "שעון" ו"פיצה", ואיזה מהם נלמד תלוי ברוחב הרשת ובקשב.
- Engels et al. 2024, "Not All Language Model Features Are Linear".
- Nanda et al. 2023, מדדי התקדמות ב־grokking (ייצוג פורייה בחשבון מודולרי).
- Zhong, Liu, Tegmark & Andreas 2023, "The Clock and the Pizza".

**מה זה אומר לנו:** "הפיצה" מחשבת *בתוך* העיגול ולא על היקפו, כלומר משתמשת באורך הווקטור ולא רק בזווית. זה תקדים מכני ישיר לכיוון 1: גם אצלנו גודל הווקטור יכול לשאת מידע. השוני הוא שאצלנו הגודל אמור לשאת ודאות של אמונה, לא פונקציה דטרמיניסטית.

### 2.3 מודלי עולם ובדיקות (probes)
- Li et al. 2023, Othello-GPT: ייצוג פנימי של הלוח.
- Gurnee & Tegmark 2024: מרחב וזמן מיוצגים ליניארית במודלי שפה.
- מהמפה הקודמת: Vafa et al. 2024 (מדדי עקביות של מודל עולם).

**מה זה אומר לנו:** לגלות ייצוג בעזרת בדיקה ליניארית כבר אינו חידוש. ההבדל שלנו הוא אורקל מדויק ובקרות שמבחינות בין ייצוג לבין שימוש.

### 2.4 תאי רשת, מקום וכיוון ראש ברשתות מאומנות
**מה ידוע:** RNN שמאומנות על אינטגרציית מסלול מפתחות יחידות דמויות תאי רשת. התאוריה מסבירה זאת כיצירת דפוסים. אבל ביקורת רחבה הראתה שזה קורה רק בבחירות צרות של יעד האימון: בפחות מ־10% מיותר מ־11,000 רשתות, ותלוי ברוחב תאי המקום שמשמשים יעד. במוח עצמו פעילות תאי רשת יושבת על טורוס, ופעילות תאי כיוון הראש על טבעת. מודל ה־TEM ומודל הטרנספורמר עם קידוד מיקום חוזר מראים שמודלים של זיכרון יחסי מפתחים תאי רשת ומקום.
- Cueva & Wei 2018, ICLR: תאים דמויי רשת ב־RNN.
- Banino et al. 2018, Nature: ניווט וקטורי עם ייצוגים דמויי רשת.
- Sorscher, Mel, Ganguli & Ocko 2019, NeurIPS: תאוריה מאחדת דרך יצירת דפוסים.
- Schaeffer, Khona & Fiete 2022, NeurIPS: "No Free Lunch", ההופעה אינה כללית.
- Whittington et al. 2020, Cell: TEM.
- Whittington, Warren & Behrens 2022, ICLR: הקשר בין טרנספורמרים להיפוקמפוס.
- Gardner et al. 2022, Nature: טורוס בתאי רשת.
- Chaudhuri et al. 2019, Nature Neuroscience: טבעת בתאי כיוון ראש.

**מה זה אומר לנו:** הוויכוח הזה הוא בדיוק השאלה של כיוון 2: האם המטרה מכריחה את הייצוג, או שהוא תוצר של בחירות ספציפיות? הלקח של Schaeffer et al. הוא שכל טענה של "אוניברסליות" חייבת לסרוק היפר־פרמטרים ולדווח באיזה שיעור מהריצות הייצוג מופיע, לא רק להראות דוגמה.

### 2.5 טופולוגיה לא טריוויאלית ולא־אוריינטבילית בייצוגים
**מה ידוע:** בקוד הטבעי נמצא בקבוק קליין: במרחב טלאי התמונות, ובהמשך גם בקוד של הקורטקס הראייתי. ברשתות מלאכותיות כמעט כל העבודה היא על מקודדים ולא על מודלי רצפים. VAE גאוסי רגיל אינו מסוגל לייצג רצועת מביוס. VAE שבנוי כמנה של גליל (כיסוי כפול) לומד אותה, אבל נוטה לקרוס בקואורדינטה אחת. מפה יחידה אינה יכולה לייצג משטח לא־אוריינטבילי, ולכן נדרשות כמה מפות. אוריינטביליות ניתנת לבדיקה לפי סימני דטרמיננטות היעקוביאן של מפות המעבר בין המפות.
- Carlsson, Ishkhanov, de Silva & Zomorodian 2008, IJCV: בקבוק קליין בטלאי תמונות.
- van Hulst, Tomczak, Heemels & Antunes 2026, arXiv:2606.07058: VAE עם טופולוגיה מוכתבת, כולל רצועת מביוס דרך כיסוי כפול.
- Paluzo-Hidalgo & Ike 2026, arXiv:2602.22873: אטלסים של מקודדים אוטומטיים ומחלקות אופייניות; בדיקת אוריינטביליות לפי סימני היעקוביאנים של מפות המעבר.
- מהמפה הקודמת: Fitz et al. 2026 ו־Malhotra et al. 2026 (הומולוגיה מתמדת של ייצוגים).

**מה זה אומר לנו:** לא מצאנו אף עבודה שבה מודל רצפים לומד עולם נסתר לא־אוריינטבילי ונבדק מול אורקל. ההשערה "כיסוי כפול אוריינטבילי ועוד ביט של צד" תואמת את מה שה־VAE צריך לקבל בכפייה. אצלנו השאלה היא אם זה נוצר מעצמו.

### 2.6 אוניברסליות ודמיון ייצוגים; סינון לפי ארכיטקטורה
**מה ידוע:** יש טענה כללית שמודלים מתכנסים לייצוג משותף, ויש כלים למדוד דמיון בין רשתות. על משימות מודל מרקוב נסתר, מודלי מצב (Mamba) מגיעים לפי דיווחים לניבוי בייסיאני אופטימלי, לפעמים טוב יותר מטרנספורמר. טרנספורמר יכול לייצג מסנן קלמן.
- Huh, Cheung, Wang & Isola 2024, ICML: "The Platonic Representation Hypothesis".
- Kornblith, Norouzi, Lee & Hinton 2019, ICML: CKA.
- Goel & Bartlett 2024, L4DC: "Can a Transformer Represent a Kalman Filter?".
- Zhang & Xing 2026, arXiv:2602.17744: Mamba וניבוי בייסיאני אופטימלי במודל מרקוב נסתר.
- Agarwal, Dalal & Misra 2025 (סעיף 2.1): השוואת LSTM מול Mamba.

**מה זה אומר לנו:** ההשוואות הקיימות מודדות *ביצועים* או מדדי דמיון כלליים. אף אחת לא שואלת אם *אותו מבנה טופולוגי וגאומטרי*, כאן המעגל עם רכיב ההיסטוריה שלו, מופיע בכל הארכיטקטורות.

### 2.7 קודי אוכלוסייה הסתברותיים: ודאות כעוצמה
**מה ידוע:** אוכלוסיית נוירונים יכולה לייצג התפלגות שלמה. בקוד פואסוני, הגבר (עוצמת התגובה) מקודד את ההפכי של השונות, ושילוב ראיות נעשה בחיבור ליניארי. ובמיוחד: בטבעת בייסיאנית לכיוון הראש, גובה הבליטה עולה עם ראיות מאשרות ויורד עם ראיות סותרות. זה "מסנן קלמן מעגלי", שהוא בדיוק הממוצע המעגלי ואורכו.
- Zemel, Dayan & Pouget 1998, Neural Computation.
- Ma, Beck, Latham & Pouget 2006, Nature Neuroscience.
- Beck et al. 2008, Neuron.
- Kutschireiter, Basnak, Wilson & Drugowitsch 2023, PNAS: "Bayesian inference in ring attractor networks".

**מה זה אומר לנו:** כיוון 1 הוא הגרסה המלאכותית של Kutschireiter et al. הם *בנו* רשת שעושה זאת. השאלה שלנו היא אם רשת שאומנה רק על ניבוי *מגלה* את זה בעצמה, ואם המעגל שמצאנו שומר את אורך הווקטור כמדד ודאות. הרמז (e) מהממצאים שלנו מצביע לשם.

### 2.8 התערבויות החלפה והפשטה סיבתית (בקצרה)
- Geiger, Lu, Icard & Potts 2021, NeurIPS: הפשטות סיבתיות והתערבויות החלפה.
- Geiger, Wu, Potts, Icard & Goodman 2024, CLeaR: חיפוש יישור מבוזר (DAS).
- מהמפה הקודמת: Wurgaft et al. 2026 והינדופור ושותפים 2026. אצלם מבנה עקום נראה לעין ובכל זאת אינו בשימוש. זו אזהרה רלוונטית לכיוון 1.

## 3. שלושת הכיוונים

### כיוון 1: גאומטריית האמונה על מעגל (המומנט המעגלי הראשון)
- **העבודה הקרובה ביותר:** Kutschireiter et al. 2023 (גובה הבליטה = ודאות, ברשת שנבנתה ביד); Ma et al. 2006 (גבר = ודאות); Shai et al. 2024 ו־Piotrowski et al. 2025 (סימפלקס אמונה מלא); Brenner et al. 2026 (ייצוגים מיושרים לווקטורי ניבוי, כולל סטטיסטיקות מספיקות, בהולך על סריג); "הפיצה" (אורך וקטור נושא מידע).
- **מה יהיה חדש:** בדיקה ישירה, מול אורקל מדויק ובמודלים שכבר קיימים, איזו *דחיסה* של האמונה המעגלית הרשת שומרת: הזווית בלבד, המומנט הראשון $E[e^{i\theta}]$ (זווית ואורך), או כמה הרמוניות פורייה. בנוסף, האם אורך הווקטור עוקב אחרי ריכוז הפוסטריור ולא אחרי משהו אחר (תדירות סמלים, נורמה כללית). ובדיקה סיבתית: שינוי האורך בלבד צריך לשנות את חדות הניבוי בלי להזיז את מיקומו. Brenner et al. מראים יישור לווקטור הניבוי כולו. הם לא מפרקים אותו לרכיבי פורייה על משתנה מחזורי, ולא בודקים אורך כוודאות.
- **הסיכון שזה כבר נעשה או טריוויאלי:** בינוני. (1) אם הסימפלקס כולו מיוצג ליניארית, כמו אצל Shai et al., אז כל מומנט ליניארי של האמונה ניתן לשליפה ליניארית כמעט מעצמו. כדי שהממצא יהיה מעניין צריך להראות שהמעגל *הוא* תת־המרחב הזה ושממדים אחרים לא נושאים את שאר האמונה, כלומר שיש דחיסה אמיתית. (2) ייתכן שהאורך מתאם לנורמה מסיבות לא רלוונטיות. צריך בקרות. (3) ברנר ושותפיו אולי כבר מכסים חלק בשכבות מסוימות. לא קראנו את הטקסט המלא שלהם.
- **דירוג חידוש: בינוני־גבוה.** השאלה הספציפית, דחיסה מעגלית של אמונה עם אורך כוודאות ברשת מאומנת מול אורקל, לא נמצאה. היא נשענת על ממצאים קיימים שלנו ועל תאוריה מוכנה ממדעי המוח, וזולה לבדיקה. היא לא מקבלת "גבוה" כי המסגרת הכללית תפוסה.

### כיוון 2: הכרח על פני ארכיטקטורות ופונקציות הפסד
- **העבודה הקרובה ביותר:** Schaeffer et al. 2022 (ההופעה תלויה ביעד); Sorscher et al. 2019; Brenner et al. 2026 (לפי המפה הקודמת, הארכיטקטורה משפיעה על הארגון ו"הגאומטריה אינה מקודדת בהכרח את טופולוגיית העולם"); Jerpelea 2026 (טבעת מופיעה ממשתנה טבעתי שנשתל); Riechers et al. 2025 ו־Agarwal et al. 2025 (טרנספורמר מול RNN ומול Mamba על אמונות); Huh et al. 2024.
- **מה יהיה חדש:** טבלה מבוקרת של טרנספורמר, LSTM/GRU ו־Mamba, כל אחד עם ניבוי של צעד אחד, ניבוי רב־צעדי ויעד גס או בלי מיקום. בכל תא נמדדים *אותם* ממצאים שכבר יש לנו: מעגל, רכיב היסטוריה מיושר לאורקל, ושימוש סיבתי. מדווחים שיעור הופעה על פני זרעים והיפר־פרמטרים, בסגנון Schaeffer.
- **הסיכון שזה כבר נעשה או טריוויאלי:** בינוני־גבוה. Brenner et al. כבר נוגעים בהשפעת הארכיטקטורה על הגאומטריה, וג'רפליה בהופעת טבעת. תוצאה חיובית ("כולם בונים מעגל") צפויה במידה רבה, כי בעולם מחזורי עם אורקל סטטיסטיקה מספיקה מחזורית היא כמעט מתבקשת. תוצאה שלילית קשה לפרש: אם ארכיטקטורה לא בונה מעגל, אולי היא פשוט לא למדה טוב. הניסיון שלנו עם המשימה שלא נלמדה מחזק את החשש. זה גם הכיוון היקר ביותר בחישוב.
- **דירוג חידוש: בינוני־נמוך.** יש ערך בטבלה שיטתית מול אורקל עם בקרות סיבתיות, אבל השאלה הכללית כבר נשאלה. החלק החדש ביותר הוא דווקא היעדים הגסים או בלי מיקום: אם המעגל שורד בהם, זה עדות לכך שהטופולוגיה של העולם, ולא פרטי היעד, היא שמכריחה אותו.

### כיוון 3: עולמות נסתרים לא־אוריינטביליים
- **העבודה הקרובה ביותר:** van Hulst et al. 2026 (Möbius VAE דרך כיסוי כפול, בכפייה); Paluzo-Hidalgo & Ike 2026 (מפה יחידה לא מספיקה; בדיקת אוריינטביליות); Carlsson et al. 2008 (קליין בקוד טבעי); Gardner et al. 2022 וטבעות וטורוסים במוח. לפי המפה הקודמת, גם בה סומן "עקביות אוריינטציה" כפער ארוך־טווח.
- **מה יהיה חדש:** מודל רצפים שמאומן רק על ניבוי, בעולם מביוס או קליין עם אורקל מדויק, ובדיקה אם הוא בונה כיסוי כפול ועוד מאפיין "צד", או ייצוג אחר. לא מצאנו אף עבודה כזו.
- **הסיכון שזה כבר נעשה או טריוויאלי:** נמוך שזה נעשה, גבוה שזה ייכשל. הניסיון הקודם שלנו הראה שהמודלים לא למדו את המשימה. בלי עיצוב מחדש, שבו ההבדל בין העולמות נראה בניבוי בטווח קצר, הכיוון עלול שוב לא להניב תשובה. יש גם סיכון של טריוויאליות: אם המעבר בתפר הופך סימן במפורש בתצפיות, "ביט הצד" נקרא ישירות מהקלט.
- **דירוג חידוש: גבוה,** בכפוף לכך שהמשימה תילמד. הסיכון הניסויי הוא הגבוה מבין השלושה.

## 4. המלצה

1. **קודם כיוון 1.** הוא זול, כי הוא רץ על מודלים קיימים מול האורקל הקיים. הוא נבנה ישירות על הרמז (e). יש לו תאוריה מוכנה (הממוצע המעגלי, הטבעת הבייסיאנית) שנותנת תחזיות כמותיות ברורות, והחידוש הספציפי שלו לא נמצא בספרות. מומלץ לכלול בקרה מפורשת מול "הסימפלקס כולו ליניארי": להראות שתת־מרחב המעגל לבדו נושא את הריכוז, ולהוסיף התערבות שמשנה רק את האורך.
2. **אחריו כיוון 3, אבל רק אחרי שלב היתכנות.** קודם מתכננים עולם מביוס שבו ההבדל מגליל נראה בניבוי, ומוודאים שמודל קטן לומד אותו. רק אחר כך מנסחים השערות. אם כיוון 1 מצליח, אפשר להשתמש בו בכיוון 3: על הכיסוי הכפול, המומנט הראשון מחליף סימן בכל מעבר תפר, וזה מבחן חד.
3. **כיוון 2 אחרון ומצומצם.** לא טבלה מלאה. רק השוואה ממוקדת: ארכיטקטורה חוזרת אחת (GRU או Mamba) ויעד אחד בלי מיקום, על העולם המקורי, עם אותם מדדים. כך מקבלים את עיקר הערך (האם המעגל וההיסטוריה שורדים) במחיר נמוך, ובלי להתחרות ישירות ב־Brenner et al.

## 5. רשימת מקורות

מקורות שסומנו [מפה] לקוחים מהמפה הקודמת (`RESEARCH_LANDSCAPE.md`), ששם אומתו. כל השאר אומתו בחיפוש עבור הסקירה הזו.

- Shai, A.S., Marzen, S.E., Teixeira, L., Gietelink Oldenziel, A., Riechers, P.M. (2024). Transformers Represent Belief State Geometry in their Residual Stream. NeurIPS 2024. https://arxiv.org/abs/2405.15943
- Piotrowski, M., Riechers, P.M., Filan, D., Shai, A.S. (2025). Constrained belief updates explain geometric structures in transformer representations. ICML 2025. https://arxiv.org/abs/2502.01954
- Riechers, P.M., Elliott, T.J., Shai, A.S. (2025). Neural networks leverage nominally quantum and post-quantum representations. https://arxiv.org/abs/2507.07432
- Agarwal, N., Dalal, S.R., Misra, V. (2025). The Bayesian Geometry of Transformer Attention. https://arxiv.org/abs/2512.22471
- Brenner, S., Knösche, T.R., Scherf, N. (2026). Predictive Statistics Shape Emergent World Representations of Grid Walkers. arXiv:2603.16689v2 [מפה]. https://arxiv.org/abs/2603.16689. הערה (אומת 2026-11-04): זו כותרת גרסה 2 (5 ביוני 2026), הנוכחית; לגרסה 1 (17 במרץ 2026) הכותרת "Grid-World Representations in Transformers Reflect Predictive Geometry".
- Jerpelea (2026). Planting a Latent Variable in Natural-Looking Text… arXiv:2608.26887 [מפה]. https://arxiv.org/abs/2608.26887
- Shai et al. (2026). Transformers learn factored representations. arXiv:2602.02385 [מפה].
- Balcells et al. (2026). Large Language Models Develop Belief State Geometry In-Context. arXiv:2609.17376 [מפה].
- Sarfati et al. (2026). The Shape of Beliefs… arXiv:2602.02315 [מפה].
- Wurgaft et al. (2026). Manifold Steering Reveals the Shared Geometry… arXiv:2605.05115 [מפה].
- Hindupur, Orgad, Fel, Ba (2026). When Models Don't Manipulate Manifolds… arXiv:2609.37680 [מפה].
- Fitz, Romero, Schneider (2026). Hidden Holes: topological aspects of language models. PMLR 282 [מפה].
- Malhotra et al. (2026). Tracking Representation Dynamics in LLMs with Persistent Homology. PMLR 334 [מפה].
- Engels, J., Liao, I., Michaud, E.J., Gurnee, W., Tegmark, M. (2024). Not All Language Model Features Are Linear. https://arxiv.org/abs/2405.14860
- Nanda, N., Chan, L., Lieberum, T., Smith, J., Steinhardt, J. (2023). Progress measures for grokking via mechanistic interpretability. ICLR 2023. https://arxiv.org/abs/2301.05217
- Zhong, Z., Liu, Z., Tegmark, M., Andreas, J. (2023). The Clock and the Pizza: Two Stories in Mechanistic Explanation of Neural Networks. NeurIPS 2023. https://arxiv.org/abs/2306.17844
- Li, K., Hopkins, A.K., Bau, D., Viégas, F., Pfister, H., Wattenberg, M. (2023). Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task. ICLR 2023. https://arxiv.org/abs/2210.13382
- Gurnee, W., Tegmark, M. (2024). Language Models Represent Space and Time. ICLR 2024. https://arxiv.org/abs/2310.02207
- Cueva, C.J., Wei, X.-X. (2018). Emergence of grid-like representations by training recurrent neural networks to perform spatial localization. ICLR 2018. https://arxiv.org/abs/1803.07770
- Banino, A. et al. (2018). Vector-based navigation using grid-like representations in artificial agents. Nature 557:429–433. doi:10.1038/s41586-018-0102-6
- Sorscher, B., Mel, G., Ganguli, S., Ocko, S. (2019). A unified theory for the origin of grid cells through the lens of pattern formation. NeurIPS 2019.
- Schaeffer, R., Khona, M., Fiete, I.R. (2022). No Free Lunch from Deep Learning in Neuroscience: A Case Study through Models of the Entorhinal-Hippocampal Circuit. NeurIPS 2022. bioRxiv doi:10.1101/2022.08.07.503109 (אומת 2026-11-04; לא נמצאה גרסת arXiv)
- Whittington, J.C.R. et al. (2020). The Tolman-Eichenbaum Machine. Cell 183(5):1249–1263. doi:10.1016/j.cell.2020.10.024
- Whittington, J.C.R., Warren, J., Behrens, T.E.J. (2022). Relating transformers to models and neural representations of the hippocampal formation. ICLR 2022. https://arxiv.org/abs/2112.04035
- Gardner, R.J. et al. (2022). Toroidal topology of population activity in grid cells. Nature 602:123–128. doi:10.1038/s41586-021-04268-7
- Chaudhuri, R., Gerçek, B., Pandey, B., Peyrache, A., Fiete, I. (2019). The intrinsic attractor manifold and population dynamics of a canonical cognitive circuit across waking and sleep. Nature Neuroscience 22:1512–1520.
- Carlsson, G., Ishkhanov, T., de Silva, V., Zomorodian, A. (2008). On the Local Behavior of Spaces of Natural Images. IJCV 76:1–12.
- van Hulst, J.S., Tomczak, J.M., Heemels, W.P.M.H., Antunes, D.J. (2026). Constructing VAE Latent Spaces with Prescribed Topology. https://arxiv.org/abs/2606.07058
- Paluzo-Hidalgo, E., Ike, Y. (2026). Learning Tangent Bundles and Characteristic Classes with Autoencoder Atlases. https://arxiv.org/abs/2602.22873 (אומת 2026-11-04)
- Huh, M., Cheung, B., Wang, T., Isola, P. (2024). The Platonic Representation Hypothesis. ICML 2024. https://arxiv.org/abs/2405.07987
- Kornblith, S., Norouzi, M., Lee, H., Hinton, G. (2019). Similarity of Neural Network Representations Revisited. ICML 2019. https://arxiv.org/abs/1905.00414
- Goel, G., Bartlett, P. (2024). Can a Transformer Represent a Kalman Filter? L4DC, PMLR 242. https://arxiv.org/abs/2312.06937
- Zhang, D., Xing, J. (2026). Bayesian Optimality of In-Context Learning with Selective State Spaces. https://arxiv.org/abs/2602.17744
- Zemel, R.S., Dayan, P., Pouget, A. (1998). Probabilistic Interpretation of Population Codes. Neural Computation 10:403–430.
- Ma, W.J., Beck, J.M., Latham, P.E., Pouget, A. (2006). Bayesian inference with probabilistic population codes. Nature Neuroscience 9:1432–1438.
- Beck, J.M. et al. (2008). Probabilistic Population Codes for Bayesian Decision Making. Neuron 60:1142–1152.
- Kutschireiter, A., Basnak, M.A., Wilson, R.I., Drugowitsch, J. (2023). Bayesian inference in ring attractor networks. PNAS 120(9):e2210622120.
- Geiger, A., Lu, H., Icard, T., Potts, C. (2021). Causal Abstractions of Neural Networks. NeurIPS 2021. https://arxiv.org/abs/2106.02997
- Geiger, A., Wu, Z., Potts, C., Icard, T., Goodman, N. (2024). Finding Alignments Between Interpretable Causal Variables and Distributed Neural Representations. CLeaR 2024, PMLR 236. https://arxiv.org/abs/2303.02536
