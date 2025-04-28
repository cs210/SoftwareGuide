import React from 'react';
import styles from './IntroHeader.module.css';

const IntroHeader = () => {
    return (
        <header className={styles.header}>
            <h1 className={styles.title}>
                <span className={styles.highlight}>2025</span>
                Software Fair
            </h1>
            <div className={styles.info}>
                <span className="font-semibold">When: </span>
                <a href="https://www.google.com/calendar/render?action=TEMPLATE&text=2025+Software+Fair&dates=20250607T223000Z/20250608T013000Z&details=&location=" className={styles.link}>
                    June 7th, 2025 from 3:30 to 6:30 PST
                </a>
            </div>
            <div className={styles.info}>
                <span className="font-semibold">Where: </span>
                <a href="https://www.campus-maps.com/stanford-university/taylor-grove-chuck/" className={styles.link}>Chuck Taylor Grove</a>
            </div>
            <div className={styles.info}>
                <span className="font-semibold">Parking Guide: </span>
                <a href="https://transportation.stanford.edu/parking-stanford/where-park/parking-stanford-campus" className={styles.link}>Map</a>
            </div>
        </header>
    );
};

export default IntroHeader;