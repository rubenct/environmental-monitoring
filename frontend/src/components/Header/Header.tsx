import styles from './Header.module.css';

export function Header() {
  return (
    <header className={styles.header}>
      <h1 className={styles.title}>Environmental Monitoring</h1>
      <p className={styles.subtitle}>Real-time environmental data dashboard</p>
    </header>
  );
}
