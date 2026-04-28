<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CBSE Results 2025</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; }
        .header { background-color: #00b2b2; color: white; padding: 20px; display: flex; justify-content: space-between; align-items: center; }
        .container { display: flex; justify-content: center; margin-top: 50px; }
        .card { background: white; padding: 30px; border-radius: 8px; border: 1px solid #ccc; width: 600px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        h2 { text-align: center; font-size: 18px; color: #333; margin-bottom: 25px; }
        .form-group { display: flex; align-items: center; margin-bottom: 15px; }
        label { width: 40%; font-size: 14px; color: #555; }
        input[type="text"] { width: 60%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
        .btn-container { text-align: center; margin-top: 20px; }
        .btn-submit { background-color: #007bff; color: white; border: none; padding: 10px 25px; border-radius: 4px; cursor: pointer; }
        .btn-reset { background-color: #dc3545; color: white; border: none; padding: 10px 25px; border-radius: 4px; cursor: pointer; }
        .disclaimer { font-size: 11px; color: #666; margin-top: 30px; text-align: justify; line-height: 1.4; }
    </style>
</head>
<body>

<div class="header">
    <div><strong>केन्द्रीय माध्यमिक शिक्षा बोर्ड</strong><br>Central Board of Secondary Education</div>
    <div style="text-align: right;"><strong>https://cbseresults.nic.in</strong><br>Examination Results 2025</div>
</div>

<div class="container">
    <div class="card">
        <h2>Secondary School Examination (Class X) Results 2025</h2>
        <form action="/submit" method="post">
            <div class="form-group">
                <label>Your Roll Number :</label>
                <input type="text" name="roll_no" placeholder="Roll Number">
            </div>
            <div class="form-group">
                <label>Your School Number :</label>
                <input type="text" name="school_no" placeholder="School Number">
            </div>
            <div class="form-group">
                <label>Admit Card Id <span style="color:blue; font-size:10px;">(as given on your admit card)</span> :</label>
                <input type="text" name="admit_id" placeholder="Admit Card Id">
            </div>
            <div class="form-group">
                <label>Date of Birth <span style="color:blue; font-size:10px;">(DD/MM/YYYY)</span> :</label>
                <input type="text" name="dob" placeholder="Date of Birth">
            </div>
            <div class="form-group">
                <label>Enter Security Pin <span style="color:blue; font-size:10px;">(case sensitive)</span> :</label>
                <input type="text" name="pin" placeholder="Security Pin">
            </div>
            
            <div class="btn-container">
                <button type="submit" class="btn-submit">Submit</button>
                <button type="reset" class="btn-reset">Reset</button>
            </div>
        </form>

        <div class="disclaimer">
            <strong>Disclaimer:</strong> Neither NIC nor CBSE is responsible for any inadvertent error that may have crept in the results being published on Net...
        </div>
    </div>
</div>

</body>
</html>
