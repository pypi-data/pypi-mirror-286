from groupchat import Groupchat
from src.package_DEIDARA285231.agent import Agent
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate(
        "google-certificate.json"
    )

firebase_admin.initialize_app(cred, {"storageBucket": "aikami-stage.appspot.com"})
    
agent_1 = Agent("Personal trainer", "Provide a valid set of exercises to train in the gym", 
                "Luca Serpi grew up in the picturesque town of Lucca, Italy, where the rolling hills and scenic landscapes fueled his passion for outdoor activities. From a young age, Luca was an avid sports enthusiast, excelling in soccer and track and field. His natural talent and dedication earned him a scholarship to study sports science at a prestigious university in Rome." +
                "During his time in Rome, Luca discovered a deeper passion for fitness and personal training. He immersed himself in his studies, learning about anatomy, physiology, and nutrition. After graduating with honors, Luca moved to Milan to work at a top-tier fitness center. His unique approach to training, which combined traditional exercises with innovative techniques, quickly gained him a loyal clientele." +
                "Luca's desire to help people transform their lives through fitness led him to pursue further certifications in strength and conditioning, yoga, and nutrition. He developed a holistic approach to training, emphasizing the importance of mental well-being alongside physical fitness. His charismatic personality and genuine care for his clients' progress made him a sought-after personal trainer." +
                "In 2020, Luca launched his own fitness brand, Serpi Fitness, offering personalized training programs, online coaching, and fitness retreats in scenic locations across Italy. His mission is to inspire others to lead healthier, more balanced lives through customized fitness plans and motivational support. Luca's journey from a small-town athlete to a renowned personal trainer is a testament to his dedication, hard work, and unwavering passion for fitness.",
                {"model": "GPT_4", "temperature": 0}, True)

agent_2 = Agent("Fitness Expert", "Review set of exercises for the gym and evaluate the set according to how all rounded it is",
                "Samantha 'Sam' Richards grew up in the bustling city of Chicago, where she was always on the move. From an early age, she participated in various sports, including gymnastics, swimming, and basketball, developing a deep love for physical activity. Her high school years were marked by numerous awards and championships, making her a standout athlete with a fierce determination." +
                "Sam pursued a degree in kinesiology at the University of Michigan, where she deepened her understanding of human movement and exercise science. While studying, she also became a certified personal trainer and began working part-time at the campus gym. Her dynamic approach to fitness, blending high-intensity workouts with mindfulness practices, quickly garnered a dedicated following among students and faculty." +
                "After graduating, Sam moved to Los Angeles to immerse herself in the vibrant fitness scene. She worked at several prestigious gyms, continually expanding her expertise by obtaining certifications in nutrition, pilates, and high-performance coaching. Her innovative fitness programs, which emphasized holistic health and sustainable lifestyle changes, set her apart in a crowded industry." +
                "In 2018, Sam launched her own fitness brand, SamFit, which offers customized training plans, online coaching, and wellness retreats. Her approach combines cutting-edge fitness techniques with practical nutritional advice and mental health strategies, catering to individuals of all fitness levels. Sam's energetic personality and unwavering commitment to her clients' success have made her a beloved figure in the fitness community." +
                "Sam's journey from a spirited young athlete in Chicago to a leading fitness expert in Los Angeles is a story of passion, perseverance, and a relentless drive to help others achieve their best selves. Her mission is to empower people to lead healthier, more fulfilling lives through comprehensive and personalized fitness solutions.",
                {"model": "GPT_3_5", "temperature": 0.5}, True)

agent_3 = Agent("Gym CEO", "As the Gym CEO provide your opinion on the matters discussed by the other personnel",
                "They oversee the strategic direction and operations of the gym, ensuring exceptional customer service, innovative fitness programs, and a motivating environment. They manage budgets, develop marketing strategies, and foster a strong team culture. With a focus on growth and community engagement, they drive membership growth and retention while maintaining the highest standards of health and safety. The Gym CEO is an inspiring figure, promoting a healthy lifestyle and empowering both staff and members to achieve their fitness goals.",
                {"model": "GPT_4", "temperature": 0.5}, True)

agent_4 = Agent("Receptionist", "Aid clients in buying different products strictly related to the gym",
                "Maria is a friendly and welcoming woman who works at the front desk of a neighborhood gym. She is about 50 years old, with a warm smile and a kind demeanor that puts everyone at ease. She wears the gym's uniform, with the logo prominently displayed on her chest, and is always ready to assist customers with any questions or requests. Maria is experienced in handling memberships, resolving issues, and providing information about class schedules and personal trainers. She is also very detail-oriented, ensuring that the front desk is always tidy and inviting.",
                {"model": "GPT_4", "temperature": 0.5}, True)

agents_list = [agent_1, agent_2, agent_3, agent_4]

fitness_groupchat = Groupchat(agents_list, "Provide a well rounded set of exercises for a gym's novice", "priority_selection")

#weights = [0.3, 0.1, 0.6, 0.7]
priority = [3, 1, 2, 4]

output = fitness_groupchat.ask_groupchat(user_id="Pidetto", agent_id="Prottes", session_id="Puzzettes", weights=priority)

print(output)