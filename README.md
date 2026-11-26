# Kosher Latvia — עותק עצמאי

עותק סטטי מלא של האתר kosher-latvia.sites.tab.bot. כל הקבצים מקומיים, אין תלות בשרת של Tab.

## מה יש כאן
- index.html — עמוד הבית (חיפוש מוצרים, חנויות, קטגוריות)
- store.html — עמוד חנות בודדת
- past.html + past-data.js — ארכיון מוצרים
- data.js — כל נתוני המוצרים (309 מוצרים פעילים) בקובץ אחד
- past-data.js — ארכיון (209 מוצרים)
- img/ — כל תמונות המוצרים (498 תמונות, מקומיות)
- design.css, styles.css, script.js, design.js — עיצוב והתנהגות
- img/ — לוגואים ואייקונים
- admin.html + admin.js — פאנל ניהול מקורי (דורש API, ראו למטה)

## הרצה מקומית
פותחים את index.html בדפדפן, או מריצים שרת קטן:
python3 -m http.server 8000

## פרסום חינם (בלי Tab)
1. Netlify Drop: נכנסים ל app.netlify.com/drop וגוררים את התיקייה. מקבלים כתובת חיה תוך דקה.
2. Cloudflare Pages: חיבור ריפו מ־GitHub, build command ריק, output dir = root.
3. GitHub Pages: מעלים את התיקייה לריפו ומפעילים Pages.
4. כל אחסון אתרים קיים שלך: מעלים את התיקייה לשורש.

## הטמעה באתר אחר
- iframe (הכי פשוט):
  <iframe src="https://הכתובת-שלך/" style="width:100%;height:80vh;border:0" loading="lazy"></iframe>
- או להעתיק את הקטעים הרצויים (header, טבלת מוצרים) אל תוך האתר הקיים, יחד עם design.css.

## עריכת עיצוב ותוכן
- צבעים, מרווחים וטיפוגרפיה: design.css ו־styles.css.
- טקסטים בכותרות: index.html.
- מוצרים: data.js (מבנה JSON בתוך window.KOSHER_DATA).
- אין צורך בכלי AI. כל עורך טקסט או VS Code מספיק.

## עדכון נתוני מוצרים
האתר מנסה לקרוא /api/data ואם אין — נופל למידע שבתוך data.js.
שלוש דרכים:
1. ידני: עורכים data.js.
2. גיליון Google: מפרסמים גיליון כ־CSV, ומוסיפים סקריפט קטן שממיר אותו ל־data.js. אפשר לעשות את זה עם Apps Script חינם.
3. בק אנד חינמי: Cloudflare Pages Functions או Netlify Functions, עם endpoints /api/data ו־/api/save. אז גם admin.html יעבוד שוב.

## מה לא עובד בגרסה סטטית
admin.html (ניהול מוצרים מהדפדפן) ורישום הסטטיסטיקות (/api/t) דורשים שרת. האתר עצמו עובד מלא בלעדיהם.

## חיבור אוטומציות חינמיות
- טפסים: Formspree, Google Forms, Web3Forms.
- גיליון נתונים: Google Sheets + Apps Script.
- אוטומציות: n8n self-hosted, Make free tier, GitHub Actions לתזמון עדכונים.
- דומיין: Netlify/Cloudflare נותנים דומיין חינם, ואפשר לחבר דומיין משלך.

## איך נכנסים לניהול
- *באתר Tab* (המקום שבו עורכים היום): https://kosher-latvia.sites.tab.bot/admin
  שם מזינים את הסיסמה שהגדרת, ושם מעדכנים מוצרים, חנויות ומחירים. השינויים נשמרים אצל Tab.
- *בעותק העצמאי*: אין מסך ניהול, כי אין שרת. שלוש דרכים:
  1. *סנכרון אוטומטי מ־Tab* (מומלץ): מריצים python3 update_from_tab.py, והעותק מושך את הנתונים והתמונות העדכניים. אין צורך בסיסמה, הנתונים פתוחים לקריאה.
  2. *עריכה ידנית*: פותחים את data.js ומשנים.
  3. *בקאנד חינמי*: Cloudflare Pages Functions או Netlify Functions, ואז admin.html עובד גם אצלך.

## סנכרון אוטומטי (בלי לגעת בקוד)
1. ידני: python3 update_from_tab.py
2. מתוזמן: הקובץ .github/workflows/sync.yml מריץ את הסנכרון כל יום ב־04:00 UTC. מעלים את התיקייה לריפו GitHub, מפעילים Actions, וזה מתעדכן לבד. אם האתר מתארח ב־GitHub Pages או ב־Cloudflare Pages שמחובר לריפו, הפרסום מתעדכן אוטומטית אחרי כל סנכרון.
3. שינוי שעה: עורכים את שורת ה־cron בקובץ.

## עמוד הניהול שלך (בלי Tab)
- הכתובת: admin.html (או admin-local.html) באתר שלך. למשל https://הדומיין-שלך/admin.html
- זה קובץ אחד עצמאי: עריכת מוצרים, הוספת מוצר, מחיקה, שיוך לחנויות, סימון אזל מהמלאי, העלאת תמונה.
- שמירה בשתי דרכים:
  1. *שמור והורד data.js*: מוריד קובץ מוכן, ואתה מחליף אותו בתיקייה ומעלה מחדש.
  2. *שמור ל-GitHub*: מעדכן את data.js ישירות בריפו. צריך למלא פעם אחת בהגדרות: בעלים, ריפו, ענף, נתיב וטוקן עם הרשאת contents. אם האתר על GitHub Pages או Cloudflare Pages, השינוי עולה לאוויר אוטומטית תוך דקה.
- אין סיסמה מובנית בעמוד הזה. אם הוא פומבי, כל מי שיש לו את הכתובת יכול לערוך בדפדפן שלו, אבל בלי טוקן GitHub הוא לא יכול לשמור לשום מקום. להגנה: כדאי להעלות את admin.html רק כשצריך, או להגן עליו בסיסמה אצל ספק האחסון (Netlify: Password protection, Cloudflare: Access).
- admin-tab-original.html הוא פאנל הניהול המקורי של Tab, הוא דורש את השרת של Tab ולא יעבוד אצלך.

## החלפת הכתובת (URL)
- את הכתובת של Tab (kosher-latvia.sites.tab.bot) אי אפשר לשנות, היא שייכת ל־Tab.
- באתר שלך הכתובת נקבעת אצל ספק האחסון:
  1. Netlify: אחרי גרירה מקבלים שם אקראי, ואפשר לשנות ב־Site configuration → Change site name, למשל kosher-latvia.netlify.app.
  2. Cloudflare Pages: בוחרים את שם הפרויקט, ומקבלים <שם>.pages.dev.
  3. GitHub Pages: <משתמש>.github.io/<ריפו>.
- דומיין משלך (למשל kosherlatvia.lv): רוכשים דומיין, ואז Netlify או Cloudflare נותנים חיבור אוטומטי עם תעודת SSL חינם.
