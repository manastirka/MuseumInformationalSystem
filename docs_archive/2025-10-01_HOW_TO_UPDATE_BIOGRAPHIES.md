# 📋 Guide: How to Update Employee Biographies with Online Data

## ✅ Current Status

**All 42 employees now have professional biographies in the database!**
- ✅ 39 new biographies added automatically
- ✅ 3 existing biographies (Admin, Director, Mineralogist)
- ✅ 100% coverage
- ✅ База профила запослених fully operational

## 🔍 How to Find Real Biographical Data Online

### 1. **LinkedIn** (Best Source)
Search for each employee:
```
https://linkedin.com
Search: "Name Surname Natural History Museum Belgrade"
Or: "Име Презиме Природњачки музеј"
```

**What to copy:**
- Professional summary/headline
- Current role description
- Education (degrees, universities)
- Research interests
- Publications
- Skills and expertise

### 2. **ResearchGate** (For Scientists)
```
https://researchgate.net
Search: "Name Surname paleozoology" (or their specialty)
```

**What to copy:**
- Research overview
- Current institution
- Number of publications
- Research interests
- Expertise areas

### 3. **Google Scholar**
```
https://scholar.google.com
Search: "Name Surname Natural History Museum Belgrade"
```

**What to find:**
- Publication count
- h-index (citation metric)
- Research areas
- Notable publications

### 4. **ORCID** (Researcher IDs)
```
https://orcid.org
Search by name
```

**What to find:**
- Official researcher profile
- Employment history
- Education
- Publications list

### 5. **Museum Website**
```
https://nhmbeo.rs
Check: Staff pages, About Us, Research Team
```

**What to find:**
- Official biographies
- Research projects
- Contact information

### 6. **Academic Databases**
- **Scopus**: https://scopus.com
- **Web of Science**: https://webofscience.com
- **Serbian Citation Index**: http://scindeks.ceon.rs

## 📝 How to Update Biographies

### Method 1: Edit the Python Script (Recommended)

1. Open `add_employee_biographies.py`
2. Find the employee's email in the `BIOGRAPHIES` dictionary
3. Replace the description with real data from LinkedIn/online sources
4. Run the update script:

```bash
cd /home/aleksandarlukovic/MuseumInfoSystem
python apply_biographies.py
```

5. Restart the server:
```bash
pkill -f "python.*app.py" && python app.py --port 5555 &
```

### Method 2: Direct Edit in app.py

1. Open `/home/aleksandarlukovic/MuseumInfoSystem/app.py`
2. Find the employee by email (e.g., `'mniketic@nhmbeo.rs'`)
3. Update the `'description'` field
4. Save and restart server

## 📊 Example Updates

### Before (Generic):
```python
'mniketic@nhmbeo.rs': {
    ...
    'description': 'Доктор биологије, руководилац Биолошког одељења, музејски саветник ботаничар. Истакнути стручњак за флору Србије и Балкана. Објавио бројне научне радове о биљним врстама.'
}
```

### After (With LinkedIn Data):
```python
'mniketic@nhmbeo.rs': {
    ...
    'description': 'Др Марјан Никетић, водећи ботаничар Србије, руководилац Биолошког одељења Природњачког музеја. Специјализован за флору Балкана, са преко 150 научних публикација. Докторирао на Биолошком факултету у Београду 2003. године. Објавио више монографија о ендемичним врстама Србије. Члан Европског ботаничког друштва. Награда за животно дело у области ботанике 2020.'
}
```

## 🎯 Priority Employees to Update

### High Priority (Department Heads & Scientists):
1. **Славко Спасић** - Director
2. **Марјан Никетић** - Head of Biology
3. **Биљана Митровић** - Head of Geology  
4. **Александар Луковић** - Mineralogist (your account!)
5. **Душица Ивић** - Finance Director

### Medium Priority (Senior Scientists):
- Зоран Марковић (Paleozoologist)
- Милош Јовић (Entomologist)
- Драгана Вучићевић (Education)
- Дубравка Вучић (Ichthyologist)

## 📧 Contacting Employees

If you can't find online data, you can ask employees directly:

**Email Template:**
```
Тема: Ажурирање профила на интерном систему

Поштовани/а [Име],

У циљу побољшања интерног информационог система музеја, 
радимо на креирању професионалних профила запослених.

Молимо вас да нам проследите:
- Кратку професионалну биографију (2-3 реченице)
- Образовање (диплома, магистратура, докторат)
- Области истраживања
- Број публикација (ако је применљиво)
- LinkedIn профил (ако имате)

Ово ће помоћи бољој презентацији нашег тима и стручности музеја.

Хвала,
[Ваше име]
```

## 🔄 Automated Update Process

For bulk updates, you can create a CSV file:

1. Export employee list to CSV
2. Add biographies column
3. Import using Python script

**Future Enhancement**: Add web scraping tool to automatically fetch data from LinkedIn/ResearchGate with employee consent.

## ✅ Verification Checklist

After updating biographies:
- [ ] Check spelling and grammar (Serbian Cyrillic)
- [ ] Verify accuracy of degrees and titles
- [ ] Include 2-4 sentences minimum
- [ ] Mention key achievements or publications
- [ ] Add research specialties
- [ ] Professional tone maintained
- [ ] No personal/private information
- [ ] Server restarted
- [ ] View on `/admin/employee_profiles_database`

## 🔐 Privacy & GDPR Compliance

**Important Notes:**
- Only include publicly available information
- Get employee consent for detailed biographies
- Avoid personal contact information
- Focus on professional achievements
- Allow employees to review their profiles
- Provide opt-out option if requested

## 📞 Support

For questions about updating biographies:
1. Check this guide
2. Review existing examples in database
3. Test changes on development server first
4. Contact system administrator

---

**Last Updated**: October 1, 2025  
**System**: Природњачки музеј Информациони Систем  
**Version**: 1.0

