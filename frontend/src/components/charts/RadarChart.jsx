import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';
import { Radar } from 'react-chartjs-2';

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

export default function RadarChart({ resultData }) {
  if (!resultData) return null;

  const data = {
    labels: [
      'Self-Awareness',
      'Self-Regulation',
      'Empathy',
      'Social Skills',
      'Motivation',
      'Stress Management',
      'Conflict Resolution',
      'Adaptability',
      'Resilience'
    ],
    datasets: [
      {
        label: 'Your EQ Profile',
        data: [
          resultData.self_awareness_score,
          resultData.self_regulation_score,
          resultData.empathy_score,
          resultData.social_skills_score,
          resultData.motivation_score,
          resultData.stress_management_score,
          resultData.conflict_resolution_score,
          resultData.adaptability_score,
          resultData.resilience_score,
        ],
        backgroundColor: 'rgba(15, 118, 110, 0.12)',
        borderColor: 'rgba(15, 118, 110, 1)',
        borderWidth: 2,
        pointBackgroundColor: '#ffffff',
        pointBorderColor: '#134e4a',
        pointHoverBackgroundColor: '#134e4a',
        pointHoverBorderColor: '#ffffff',
        pointRadius: 4,
        pointHoverRadius: 6,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      r: {
        angleLines: {
          color: 'rgba(83, 96, 93, 0.16)',
        },
        grid: {
          color: 'rgba(83, 96, 93, 0.16)',
        },
        pointLabels: {
          color: '#53605d',
          font: {
            size: 11,
            family: "'Inter', sans-serif",
          },
        },
        ticks: {
          color: 'transparent',
          backdropColor: 'transparent',
          min: 0,
          max: 100,
          stepSize: 20,
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: 'rgba(23, 32, 31, 0.92)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: 'rgba(15, 118, 110, 0.35)',
        borderWidth: 1,
        padding: 12,
        displayColors: false,
        callbacks: {
          label: function(context) {
            return `Score: ${context.raw}/100`;
          }
        }
      }
    },
  };

  return <Radar data={data} options={options} />;
}
