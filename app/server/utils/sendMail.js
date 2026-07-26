const nodemailer = require('nodemailer');

const sendMail = async (otp, email) => {
    try {
        const transport = nodemailer.createTransport({
            service: 'gmail',
            auth: {
                user: process.env.EMAIL_USER,
                pass: process.env.EMAIL_PASS
            }
        });

        const mailOptions = {
            from: process.env.EMAIL_USER,
            to: email,
            subject: 'OTP for Password Reset',
            text: `Your OTP for password reset is ${otp}. It is valid for 5 minutes.`
        };

        const info = await transport.sendMail(mailOptions);
        console.log('Email sent successfully:', info.response);
        return info;

    } catch (error) {
        console.error('Error sending email:', error.message);
        throw error; // Re-throw to handle in route controller
    }
};

module.exports = sendMail;