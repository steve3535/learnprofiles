document.addEventListener('DOMContentLoaded', function() {
    // Variables globales
    const form = document.getElementById('learning-profile-form');
    const sections = document.querySelectorAll('.question-section');
    const progressBar = document.querySelector('.progress-bar');
    const resultsSection = document.getElementById('results-section');
    const nextButtons = document.querySelectorAll('.next-btn');
    const prevButtons = document.querySelectorAll('.prev-btn');
    const restartButton = document.getElementById('restart-btn');
    
    let currentSection = 0;
    
    // Initialisation
    progressBar.style.width = '0%';
    progressBar.setAttribute('aria-valuenow', 0);
    progressBar.textContent = '0%';
    updateProgress();
    
    // Événements pour les boutons suivant/précédent
    nextButtons.forEach(button => {
        button.addEventListener('click', goToNextSection);
    });
    
    prevButtons.forEach(button => {
        button.addEventListener('click', goToPrevSection);
    });
    
    // Événement pour le bouton recommencer
    restartButton.addEventListener('click', restartQuiz);
    
    // Soumission du formulaire
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Vérifier si toutes les questions sont répondues
        if (!validateForm()) {
            alert('Veuillez répondre à toutes les questions avant de soumettre.');
            return;
        }
        
        // Mettre à jour la barre de progression à 100%
        progressBar.style.width = '100%';
        progressBar.setAttribute('aria-valuenow', 100);
        progressBar.textContent = '100%';
        
        // Calculer les scores
        const scores = calculateScores();
        
        // Afficher les résultats
        displayResults(scores);
        
        // Envoyer les résultats par email
        sendResultsByEmail(scores);
    });
    
    // Fonctions
    function goToNextSection() {
        // Vérifier si toutes les questions de la section actuelle sont répondues
        const currentSectionElement = sections[currentSection];
        const questionGroups = {};
        
        // Regrouper les inputs par nom de question
        const radioInputs = currentSectionElement.querySelectorAll('input[type="radio"]');
        radioInputs.forEach(input => {
            const name = input.getAttribute('name');
            if (!questionGroups[name]) {
                questionGroups[name] = {
                    inputs: [],
                    answered: false
                };
            }
            questionGroups[name].inputs.push(input);
        });
        
        // Vérifier si chaque groupe de questions a au moins une réponse cochée
        let allAnswered = true;
        let unansweredQuestions = [];
        
        for (const name in questionGroups) {
            const isAnswered = questionGroups[name].inputs.some(input => input.checked);
            questionGroups[name].answered = isAnswered;
            
            if (!isAnswered) {
                allAnswered = false;
                unansweredQuestions.push(name);
            }
        }
        
        if (!allAnswered) {
            alert('Veuillez répondre à toutes les questions avant de continuer.');
            return;
        }
        
        // Passer à la section suivante
        if (currentSection < sections.length - 1) {
            sections[currentSection].style.display = 'none';
            currentSection++;
            sections[currentSection].style.display = 'block';
            updateProgress();
        }
    }
    
    function goToPrevSection() {
        if (currentSection > 0) {
            sections[currentSection].style.display = 'none';
            currentSection--;
            sections[currentSection].style.display = 'block';
            updateProgress();
        }
    }
    
    function updateProgress() {
        // La première section (index 0) correspond à 0%
        // Chaque section suivante ajoute 20% jusqu'à la dernière qui est à 80%
        // Le 100% est atteint uniquement après la soumission
        const progress = currentSection * 20;
        progressBar.style.width = `${progress}%`;
        progressBar.setAttribute('aria-valuenow', progress);
        progressBar.textContent = `${Math.round(progress)}%`;
    }
    
    function validateForm() {
        // Vérifier si toutes les questions ont été répondues
        let allAnswered = true;
        
        // Parcourir toutes les sections
        for (let i = 0; i < sections.length; i++) {
            const section = sections[i];
            const questionGroups = {};
            
            // Regrouper les inputs par nom de question
            const radioInputs = section.querySelectorAll('input[type="radio"]');
            radioInputs.forEach(input => {
                const name = input.getAttribute('name');
                if (!questionGroups[name]) {
                    questionGroups[name] = {
                        inputs: [],
                        answered: false
                    };
                }
                questionGroups[name].inputs.push(input);
            });
            
            // Vérifier si chaque groupe de questions a au moins une réponse cochée
            for (const name in questionGroups) {
                const isAnswered = questionGroups[name].inputs.some(input => input.checked);
                if (!isAnswered) {
                    allAnswered = false;
                    break;
                }
            }
            
            if (!allAnswered) {
                break;
            }
        }
        
        // Vérifier l'email
        const emailInput = document.getElementById('email');
        if (emailInput && !emailInput.value) {
            allAnswered = false;
        }
        
        return allAnswered;
    }
    
    function calculateScores() {
        const formData = new FormData(form);
        let visualCount = 0;
        let auditoryCount = 0;
        let kinestheticCount = 0;
        let logicalCount = 0;
        
        // Compter les réponses par type
        for (const [name, value] of formData.entries()) {
            if (name.startsWith('q') && name !== 'email') {
                switch (value) {
                    case 'a':
                        visualCount++;
                        break;
                    case 'b':
                        auditoryCount++;
                        break;
                    case 'c':
                        kinestheticCount++;
                        break;
                    case 'd':
                        logicalCount++;
                        break;
                }
            }
        }
        
        // Calculer les pourcentages
        const total = visualCount + auditoryCount + kinestheticCount + logicalCount;
        const visualPercent = (visualCount / total) * 100;
        const auditoryPercent = (auditoryCount / total) * 100;
        const kinestheticPercent = (kinestheticCount / total) * 100;
        const logicalPercent = (logicalCount / total) * 100;
        
        // Déterminer le style principal
        const scores = {
            visual: {
                count: visualCount,
                percent: visualPercent,
                name: 'Visuel',
                description: 'Tu apprends mieux en voyant, lisant et visualisant l\'information.',
                recommendations: [
                    'Utilise des diagrammes, des graphiques et des cartes mentales',
                    'Code tes notes par couleur pour organiser l\'information',
                    'Visualise les concepts dans ton esprit',
                    'Utilise des applications de flashcards visuelles'
                ]
            },
            auditory: {
                count: auditoryCount,
                percent: auditoryPercent,
                name: 'Auditif',
                description: 'Tu apprends mieux en écoutant, discutant et traitant verbalement.',
                recommendations: [
                    'Enregistre les cours et réécoute-les',
                    'Participe à des groupes d\'étude pour discuter des concepts',
                    'Lis à voix haute lorsque tu étudies',
                    'Explique les concepts à quelqu\'un d\'autre'
                ]
            },
            kinesthetic: {
                count: kinestheticCount,
                percent: kinestheticPercent,
                name: 'Kinesthésique',
                description: 'Tu apprends mieux par des activités pratiques, le mouvement et l\'engagement physique.',
                recommendations: [
                    'Intègre le mouvement dans ton étude (marche en révisant)',
                    'Utilise des objets physiques pour représenter des concepts',
                    'Prends des pauses actives fréquentes',
                    'Crée des modèles ou des maquettes pour comprendre les concepts'
                ]
            },
            logical: {
                count: logicalCount,
                percent: logicalPercent,
                name: 'Logique/Séquentiel',
                description: 'Tu apprends mieux par des approches organisées et systématiques avec une structure claire.',
                recommendations: [
                    'Organise ton matériel d\'étude de manière séquentielle',
                    'Établis des horaires d\'étude structurés',
                    'Décompose les concepts complexes en étapes logiques',
                    'Utilise des listes et des plans détaillés'
                ]
            }
        };
        
        // Déterminer le style principal
        let primaryStyle = 'visual';
        let maxCount = visualCount;
        
        if (auditoryCount > maxCount) {
            primaryStyle = 'auditory';
            maxCount = auditoryCount;
        }
        if (kinestheticCount > maxCount) {
            primaryStyle = 'kinesthetic';
            maxCount = kinestheticCount;
        }
        if (logicalCount > maxCount) {
            primaryStyle = 'logical';
            maxCount = logicalCount;
        }
        
        scores.primaryStyle = primaryStyle;
        
        return scores;
    }
    
    function displayResults(scores) {
        // Masquer le formulaire et afficher les résultats
        form.style.display = 'none';
        resultsSection.style.display = 'block';
        
        // Mettre à jour les barres de progression
        const visualScoreBar = document.getElementById('visual-score');
        const auditoryScoreBar = document.getElementById('auditory-score');
        const kinestheticScoreBar = document.getElementById('kinesthetic-score');
        const logicalScoreBar = document.getElementById('logical-score');
        
        visualScoreBar.style.width = `${scores.visual.percent}%`;
        visualScoreBar.setAttribute('aria-valuenow', scores.visual.percent);
        visualScoreBar.textContent = `Visuel: ${Math.round(scores.visual.percent)}%`;
        
        auditoryScoreBar.style.width = `${scores.auditory.percent}%`;
        auditoryScoreBar.setAttribute('aria-valuenow', scores.auditory.percent);
        auditoryScoreBar.textContent = `Auditif: ${Math.round(scores.auditory.percent)}%`;
        
        kinestheticScoreBar.style.width = `${scores.kinesthetic.percent}%`;
        kinestheticScoreBar.setAttribute('aria-valuenow', scores.kinesthetic.percent);
        kinestheticScoreBar.textContent = `Kinesthésique: ${Math.round(scores.kinesthetic.percent)}%`;
        
        logicalScoreBar.style.width = `${scores.logical.percent}%`;
        logicalScoreBar.setAttribute('aria-valuenow', scores.logical.percent);
        logicalScoreBar.textContent = `Logique: ${Math.round(scores.logical.percent)}%`;
        
        // Mettre à jour le style principal
        const primaryStyleName = document.getElementById('primary-style-name');
        const primaryStyleDescription = document.getElementById('primary-style-description');
        const primaryStyleDiv = document.getElementById('primary-style');
        
        primaryStyleName.textContent = scores[scores.primaryStyle].name;
        primaryStyleDescription.textContent = scores[scores.primaryStyle].description;
        
        // Ajouter la classe de style appropriée
        primaryStyleDiv.className = '';
        primaryStyleDiv.classList.add(`${scores.primaryStyle}-style`);
    }
    
    function sendResultsByEmail(scores) {
        const email = document.getElementById('email').value;
        
        // Créer une analyse détaillée pour chaque style d'apprentissage
        const detailedAnalysis = `
ANALYSE DÉTAILLÉE DU PROFIL D'APPRENTISSAGE

Style principal : ${scores[scores.primaryStyle].name} (${Math.round(scores[scores.primaryStyle].percent)}%)

RÉPARTITION DES STYLES :
- Visuel : ${Math.round(scores.visual.percent)}%
- Auditif : ${Math.round(scores.auditory.percent)}%
- Kinesthésique : ${Math.round(scores.kinesthetic.percent)}%
- Logique : ${Math.round(scores.logical.percent)}%

ANALYSE DU STYLE VISUEL (${Math.round(scores.visual.percent)}%) :
${getDetailedAnalysisForStyle('visual', scores.visual.percent)}

ANALYSE DU STYLE AUDITIF (${Math.round(scores.auditory.percent)}%) :
${getDetailedAnalysisForStyle('auditory', scores.auditory.percent)}

ANALYSE DU STYLE KINESTHÉSIQUE (${Math.round(scores.kinesthetic.percent)}%) :
${getDetailedAnalysisForStyle('kinesthetic', scores.kinesthetic.percent)}

ANALYSE DU STYLE LOGIQUE (${Math.round(scores.logical.percent)}%) :
${getDetailedAnalysisForStyle('logical', scores.logical.percent)}

RECOMMANDATIONS PERSONNALISÉES POUR LE STYLE ${scores[scores.primaryStyle].name.toUpperCase()} :
- ${getExpandedRecommendations(scores.primaryStyle).join('\n- ')}

RECOMMANDATIONS POUR ÉQUILIBRER LES STYLES :
- ${getBalancingRecommendations(scores).join('\n- ')}

IMPLICATIONS POUR LE COACHING :
- ${getCoachingImplications(scores).join('\n- ')}
`;

        console.log("Envoi d'email avec les données suivantes:", {
            to_email: "coach@dianatape.com",
            user_email: email,
            visual_score: Math.round(scores.visual.percent),
            auditory_score: Math.round(scores.auditory.percent),
            kinesthetic_score: Math.round(scores.kinesthetic.percent),
            logical_score: Math.round(scores.logical.percent),
            primary_style: scores[scores.primaryStyle].name
        });

        // Préparer le contenu de l'email
        const templateParams = {
            to_email: "coach@dianatape.com",
            from_name: "Évaluation du Profil d'Apprentissage",
            to_name: "Coach",
            user_email: email,
            visual_score: Math.round(scores.visual.percent),
            auditory_score: Math.round(scores.auditory.percent),
            kinesthetic_score: Math.round(scores.kinesthetic.percent),
            logical_score: Math.round(scores.logical.percent),
            primary_style: scores[scores.primaryStyle].name,
            primary_description: scores[scores.primaryStyle].description,
            detailed_analysis: detailedAnalysis,
            recommendations: getExpandedRecommendations(scores.primaryStyle).join('\n- ')
        };
        
        // Envoyer l'email avec vos identifiants
        emailjs.send('service_b9hata3', 'template_jwefp5f', templateParams)
            .then(function(response) {
                console.log('Email envoyé avec succès!', response.status, response.text);
            }, function(error) {
                console.log('Échec de l\'envoi de l\'email...', error);
                alert('Une erreur est survenue lors de l\'envoi de l\'email. Vos résultats sont toujours affichés sur cette page.');
            });
    }
    
    // Fonction pour obtenir une analyse détaillée en fonction du pourcentage
    function getDetailedAnalysisForStyle(style, percent) {
        const styleNames = {
            visual: 'visuel',
            auditory: 'auditif',
            kinesthetic: 'kinesthésique',
            logical: 'logique'
        };
        
        const styleName = styleNames[style];
        
        if (percent >= 40) {
            return `Le style ${styleName} est dominant dans le profil d'apprentissage. Cela indique une forte préférence pour les méthodes d'apprentissage ${styleName}s. Cette force peut être exploitée pour maximiser l'efficacité de l'apprentissage.`;
        } else if (percent >= 25) {
            return `Le style ${styleName} est modérément présent dans le profil d'apprentissage. Il représente une voie d'apprentissage efficace qui peut être développée davantage.`;
        } else {
            return `Le style ${styleName} est moins présent dans le profil d'apprentissage. Développer des compétences dans ce domaine pourrait aider à équilibrer les approches d'apprentissage.`;
        }
    }
    
    // Fonction pour obtenir des recommandations étendues
    function getExpandedRecommendations(style) {
        const baseRecommendations = {
            visual: [
                'Utiliser des diagrammes, des graphiques et des cartes mentales pour organiser l\'information',
                'Coder les notes par couleur pour faciliter la mémorisation et la catégorisation',
                'Visualiser les concepts dans l\'esprit avant les examens',
                'Utiliser des applications de flashcards visuelles pour la révision',
                'Créer des affiches ou des aide-mémoire visuels pour les concepts clés',
                'Regarder des vidéos éducatives sur les sujets difficiles',
                'Transformer les informations textuelles en diagrammes ou en infographies',
                'Utiliser des surligneurs de différentes couleurs pour structurer les notes',
                'S\'asseoir à l\'avant de la classe pour mieux voir les présentations',
                'Demander aux enseignants des supports visuels supplémentaires'
            ],
            auditory: [
                'Enregistrer les cours et les réécouter pendant les révisions',
                'Participer activement aux discussions de groupe pour verbaliser les concepts',
                'Lire à voix haute lors de l\'étude de nouveaux matériaux',
                'Expliquer les concepts à d\'autres personnes pour renforcer la compréhension',
                'Utiliser des podcasts éducatifs comme ressource supplémentaire',
                'Créer des chansons ou des rimes pour mémoriser des informations',
                'Participer à des débats sur les sujets étudiés',
                'Utiliser la technique de récitation pour mémoriser des informations',
                'Étudier dans un environnement avec un léger bruit de fond',
                'Enregistrer ses propres explications et les réécouter'
            ],
            kinesthetic: [
                'Intégrer le mouvement dans les sessions d\'étude (marcher en révisant)',
                'Utiliser des objets manipulables pour représenter des concepts',
                'Prendre des pauses actives fréquentes pendant les longues sessions d\'étude',
                'Apprendre par la pratique et l\'expérimentation directe',
                'Utiliser des gestes pour associer des mouvements aux concepts clés',
                'Créer des modèles physiques pour les concepts complexes',
                'Alterner entre différentes positions physiques pendant l\'étude',
                'Participer à des simulations ou des jeux de rôle éducatifs',
                'Utiliser des techniques de respiration pour maintenir la concentration',
                'Associer des mouvements spécifiques à des informations à mémoriser'
            ],
            logical: [
                'Organiser l\'information en catégories et sous-catégories logiques',
                'Créer des systèmes et des structures pour aborder les problèmes complexes',
                'Utiliser des techniques de résolution de problèmes étape par étape',
                'Rechercher les relations de cause à effet dans les sujets étudiés',
                'Développer des arguments pour et contre pour approfondir la compréhension',
                'Utiliser des applications de planification pour structurer le temps d\'étude',
                'Décomposer les concepts complexes en éléments plus simples',
                'Rechercher les modèles et les tendances dans les informations',
                'Poser des questions "pourquoi" et "comment" pour approfondir la compréhension',
                'Créer des listes de contrôle pour suivre la progression de l\'apprentissage'
            ]
        };
        
        return baseRecommendations[style];
    }
    
    // Fonction pour obtenir des recommandations d'équilibrage
    function getBalancingRecommendations(scores) {
        const styles = ['visual', 'auditory', 'kinesthetic', 'logical'];
        const lowestStyle = styles.reduce((a, b) => scores[a].percent < scores[b].percent ? a : b);
        
        const balancingRecommendations = {
            visual: [
                'Intégrer plus d\'éléments visuels dans les méthodes d\'étude actuelles',
                'Essayer de convertir les notes textuelles en diagrammes ou en cartes mentales',
                'Utiliser le code couleur pour organiser les informations',
                'Regarder des vidéos éducatives en complément des lectures'
            ],
            auditory: [
                'Pratiquer l\'explication verbale des concepts appris',
                'Rejoindre ou former un groupe d\'étude pour discuter des sujets',
                'Enregistrer et réécouter les points clés des leçons',
                'Lire les textes importants à voix haute plutôt que silencieusement'
            ],
            kinesthetic: [
                'Incorporer plus de mouvement pendant les sessions d\'étude',
                'Utiliser des objets manipulables pour représenter des concepts abstraits',
                'Prendre des pauses actives régulières pendant l\'étude',
                'Essayer d\'étudier en marchant ou en bougeant légèrement'
            ],
            logical: [
                'Développer des systèmes de classification pour organiser l\'information',
                'Rechercher les relations logiques entre les différents concepts',
                'Pratiquer la résolution de problèmes étape par étape',
                'Créer des listes et des tableaux pour structurer l\'information'
            ]
        };
        
        return balancingRecommendations[lowestStyle];
    }
    
    // Fonction pour obtenir des implications pour le coaching
    function getCoachingImplications(scores) {
        const primaryStyle = scores.primaryStyle;
        
        const coachingImplications = {
            visual: [
                'Utiliser des supports visuels lors des sessions de coaching',
                'Encourager la création de tableaux de visualisation pour les objectifs',
                'Fournir des documents écrits avec des éléments visuels pour renforcer les concepts',
                'Aider à développer des techniques de visualisation pour la performance'
            ],
            auditory: [
                'Privilégier les discussions verbales pendant les sessions de coaching',
                'Encourager l\'auto-dialogue positif et les affirmations',
                'Proposer des enregistrements audio comme ressources supplémentaires',
                'Utiliser des techniques de questionnement pour stimuler la réflexion verbale'
            ],
            kinesthetic: [
                'Intégrer des activités physiques dans les sessions de coaching',
                'Encourager l\'apprentissage par l\'expérience directe',
                'Utiliser des exercices pratiques pour illustrer les concepts',
                'Reconnaître le besoin de mouvement et l\'intégrer dans le plan d\'action'
            ],
            logical: [
                'Présenter des plans d\'action structurés et logiques',
                'Aider à développer des systèmes d\'organisation personnalisés',
                'Fournir des explications détaillées du "pourquoi" derrière les recommandations',
                'Utiliser des approches analytiques pour résoudre les problèmes'
            ]
        };
        
        return coachingImplications[primaryStyle];
    }
    
    function restartQuiz() {
        // Réinitialiser le formulaire
        form.reset();
        
        // Revenir à la première section
        sections.forEach(section => {
            section.style.display = 'none';
        });
        sections[0].style.display = 'block';
        currentSection = 0;
        
        // Mettre à jour la barre de progression
        updateProgress();
        
        // Masquer les résultats et afficher le formulaire
        resultsSection.style.display = 'none';
        form.style.display = 'block';
    }
});
