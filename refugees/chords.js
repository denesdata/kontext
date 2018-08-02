/*//////////////////////////////////////////////////////////
////////////////// Set up the Data /////////////////////////
//////////////////////////////////////////////////////////*/

var NameProvider = ["Lebanon","Jordan","Germany","Ethiopia","Iraq","Iran","Kenya","Turkey"];
	
var matrix = [
[9.6899,0.8859,0.0554,0.443,2.5471,2.4363,0.5537,2.5471], /*Apple 19.1584*/
[0.1107,1.8272,0,0.4983,1.1074,1.052,0.2215,0.4983], /*HTC 5.3154*/
[0.0554,0.2769,0.2215,0.2215,0.3876,0.8306,0.0554,0.3322], /*Huawei 2.3811*/
[0.0554,0.1107,0.0554,1.2182,1.1628,0.6645,0.4983,1.052], /*LG 4.8173*/
[0.2215,0.443,0,0.2769,10.4097,1.2182,0.4983,2.8239], /*Nokia 15.8915*/
[1.1628,2.6024,0,1.3843,8.7486,16.8328,1.7165,5.5925], /*Samsung 38.0399*/
[0.0554,0.4983,0,0.3322,0.443,0.8859,1.7719,0.443], /*Sony 4.4297*/
[0.2215,0.7198,0,0.3322,1.6611,1.495,0.1107,5.4264] /*Other 9.9667*/
];
/*Sums up to exactly 100*/

var colors = ['#DD1367','#ccc','#4C9F38','#C5192D','#FF3A21','#26BDE2','#3F7E44','#FD9D24'];

color1="#418FDE";
color2="#00497A";
bgcolor="#00233A"
op1=0.9;

/*Initiate the color scale*/
var fill = d3.scale.ordinal()
    .domain(d3.range(NameProvider.length))
    .range(colors);
	
/*//////////////////////////////////////////////////////////
/////////////// Initiate Chord Diagram /////////////////////
//////////////////////////////////////////////////////////*/

var width = 685,
    height = 550,
	hPad = 50
    innerRadius = Math.min(width, height) * .39,
    outerRadius = innerRadius * 1.04;

/*Initiate the SVG*/
var svg = d3.select("#chart").append("svg:svg")
    .attr("width", width+50)
    .attr("height", height+70)
	.append("svg:g")
    .attr("transform", "translate(" + width / 2 + "," + (height / 2 + hPad) + ")");

	
var chord = d3.layout.chord()
    .padding(.04)
    .sortSubgroups(d3.descending) /*sort the chords inside an arc from high to low*/
    .sortChords(d3.descending) /*which chord should be shown on top when chords cross. Now the biggest chord is at the bottom*/
	.matrix(matrix);
	

/*//////////////////////////////////////////////////////////
////////////////// Draw outer Arcs /////////////////////////
//////////////////////////////////////////////////////////*/

var arc = d3.svg.arc()
    .innerRadius(innerRadius)
    .outerRadius(outerRadius);
	
var g = svg.selectAll("g.group")
	.data(chord.groups)
	.enter().append("svg:g")
	.attr("class", function(d) {return "group " + NameProvider[d.index];});
	
g.append("svg:path")
	  .attr("class", "arc")
	  .style("stroke", function(d) { return fill(d.index); })
	  .style("fill", function(d) { return fill(d.index); })
	  .attr("d", arc)
	  .style("opacity", 0)
	  .transition().duration(1000)
	  .style("opacity", 0.4);

/*//////////////////////////////////////////////////////////
////////////////// Initiate Ticks //////////////////////////
//////////////////////////////////////////////////////////*/

var ticks = svg.selectAll("g.group").append("svg:g")
	.attr("class", function(d) {return "ticks " + NameProvider[d.index];})
	.selectAll("g.ticks")
	.attr("class", "ticks")
    .data(groupTicks)
	.enter().append("svg:g")
    .attr("transform", function(d) {
      return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
          + "translate(" + outerRadius+40 + ",0)";
    });

/*Append the tick around the arcs*/
ticks.append("svg:line")
	.attr("x1", 1)
	.attr("y1", 0)
	.attr("x2", 5)
	.attr("y2", 0)
	.attr("class", "ticks")
	.style("stroke", color1);
	
/*Add the labels for the %'s*/
ticks.append("svg:text")
	.attr("x", 8)
	.attr("dy", ".35em")
	.attr("class", "tickLabels")
	.attr("transform", function(d) { return d.angle > Math.PI ? "rotate(180)translate(-16)" : null; })
	.style("text-anchor", function(d) { return d.angle > Math.PI ? "end" : null; })
	.text(function(d) { return d.label; })
	.attr('opacity', 0);
	
/*//////////////////////////////////////////////////////////
////////////////// Initiate Names //////////////////////////
//////////////////////////////////////////////////////////*/

g.append("svg:text")
  .each(function(d) { d.angle = (d.startAngle + d.endAngle) / 2; })
  .attr("dy", ".35em")
  .attr("class", "titles")
  .attr("text-anchor", function(d) { return d.angle > Math.PI ? "end" : null; })
  .attr("transform", function(d) {
		return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
		+ "translate(" + (innerRadius + 55) + ")"
		+ (d.angle > Math.PI ? "rotate(180)" : "");
  })
  .attr('opacity', 0)
  .text(function(d,i) { return NameProvider[i]; });  

/*//////////////////////////////////////////////////////////
//////////////// Initiate inner chords /////////////////////
//////////////////////////////////////////////////////////*/

var chords = svg.selectAll("path.chord")
	.data(chord.chords)
	.enter().append("svg:path")
	.attr("class", "chord")
	.style("stroke", function(d) { return d3.rgb(fill(d.source.index)).darker(); })
	.style("fill", function(d) { return fill(d.source.index); })
	.attr("d", d3.svg.chord().radius(innerRadius))
	.attr('opacity', 0);

/*//////////////////////////////////////////////////////////	
///////////// Initiate Progress Bar ////////////////////////
//////////////////////////////////////////////////////////*/
/*Initiate variables for bar*/
var progressColor = ["#00497A","#0072BC"],
	progressClass = ["prgsBehind","prgsFront"],
	prgsWidth = 0.4*650,
	prgsHeight = 3;
/*Create SVG to visualize bar in*/
var progressBar = d3.select("#progress").append("svg")
	.attr("width", prgsWidth)
	.attr("height", 3*prgsHeight);
/*Create two bars of which one has a width of zero*/
progressBar.selectAll("rect")
	.data([prgsWidth, 0])
	.enter()
	.append("rect")
	.attr("class", function(d,i) {return progressClass[i];})
	.attr("x", 0)
	.attr("y", 0)
	.attr("width", function (d) {return d;})
	.attr("height", prgsHeight)
	.attr("fill", function(d,i) {return progressColor[i];});

/*//////////////////////////////////////////////////////////	
/////////// Initiate the Center Texts //////////////////////
//////////////////////////////////////////////////////////*/
/*Create wrapper for center text*/
var textCenter = svg.append("g")
					.attr("class", "explanationWrapper");

/*Starting text middle top*/
var middleTextTop = textCenter.append("text")
	.attr("class", "explanation")
	.attr("text-anchor", "middle")
	.attr("x", 0 + "px")
	.attr("y", -24*10/2 + "px")
	.attr("dy", "1em")
	.attr("opacity", 1)
	.text("This visualization maps the refugee flows between source and target countries during the period 1951-2014, using a chord diagram layout.")
	.call(wrap, 350);

/*Starting text middle bottom*/
var middleTextBottom = textCenter.append("text")
	.attr("class", "explanation")
	.attr("text-anchor", "middle")
	.attr("x", 0 + "px")
	.attr("y", 24*3/2 + "px")
	.attr("dy", "1em")
	.attr('opacity', 1)
	.text("This tutorial explains how to read the chord diagrams, and offers you navigation advice for this website.")
	.call(wrap, 350);


/*//////////////////////////////////////////////////////////
//////////////// Storyboarding Steps ///////////////////////
//////////////////////////////////////////////////////////*/

var counter = 1,
	buttonTexts = ["Ok","Go on","Continue","Okay","Go on","Continue","Okay","Continue",
				   "Continue","Continue","Continue","Continue","Continue","Finish","Okay","Okay","Enter app"],
	opacityValueBase = 0.8,
	opacityValue = 0.4;

/*Reload page*/
d3.select("#reset")
	.on("click", function(e) {location.reload();});

/*Skip to final visual right away*/
d3.select("#skip")
	.on("click", finalChord);
	
/*Order of steps when clicking button*/
d3.select("#clicker")      
	.on("click", function(e){
	
		if(counter == 1) Draw1();
		else if(counter == 2) Draw2();
		else if(counter == 3) Draw3();
		else if(counter == 4) Draw4();
		else if(counter == 5) Draw5();
		else if(counter == 6) Draw6();
		else if(counter == 7) Draw7();
		else if(counter == 8) Draw8();
		else if(counter == 9) Draw9();
		else if(counter == 10) Draw10();
		else if(counter == 11) Draw11();
		else if(counter == 12) Draw12();
		else if(counter == 13) Draw13();
		else if(counter == 14) Draw14();
		else if(counter == 15) Draw15();
		else if(counter == 16) Draw16();
		else if(counter == 17) Draw17();
		else if(counter == 18) finalChord();
		
		counter = counter + 1;
	});

/*//////////////////////////////////////////////////////////	
//Introduction
///////////////////////////////////////////////////////////*/
function Draw1(){

	/*First disable click event on clicker button*/
	stopClicker();
		
	/*Show and run the progressBar*/
	runProgressBar(time=700*11);
		
	changeTopText(newText = "These days perhaps the biggest global media topic is refugees and immigrants. " + 
							"There are refugee cryses in Europe, the Middle East, Central Africa, Southeast Asia...",
	loc = 4/2, delayDisappear = 0, delayAppear = 1);

	changeTopText(newText = "In the next few steps I would like to introduce you to the flows of people between the source and target countries or territories.",
	loc = 10/2, delayDisappear = 9, delayAppear = 10, finalText = true);
	
	changeBottomText(newText = "Let's start by drawing out the division of the world's 50+ million refugees, who have requested asylum or reside in foreign countries or territories (UN).",
	loc = 1/2, delayDisappear = 0, delayAppear = 10);
	
	//Remove arcs again
	d3.selectAll(".arc")
		.transition().delay(9*700).duration(2100)
		.style("opacity", 0)
		.each("end", function() {d3.selectAll(".arc").remove();});
		
};/*Draw1*/

/*//////////////////////////////////////////////////////////	
//Show Arc of Apple
//////////////////////////////////////////////////////////*/
function Draw2(){ 

	/*First disable click event on clicker button*/
	stopClicker();
	
	/*Show and run the progressBar*/
	runProgressBar(time=700*2);
				
	/*Initiate all arcs but only show the Apple arc (d.index = 0)*/
	g.append("svg:path")
	  .style("stroke", function(d) { return fill(d.index); })
	  .style("fill", function(d) { return fill(d.index); })
	  .transition().duration(700)
	  .attr("d", arc)
	  .style("opacity", op1)
	  .attrTween("d", function(d) {
		if(d.index == 0) {
		   var i = d3.interpolate(d.startAngle, d.endAngle);
		   return function(t) {
			   d.endAngle = i(t);
			 return arc(d);
		   }
		}
	  });
	  
	/*Show the tick around the Apple arc*/
	d3.selectAll("g.group").selectAll("line")
		.transition().delay(700).duration(1000)
		.style("stroke", function(d, i, j) {return j ? 0 : color1; });

	/*Add the labels for the %'s at Apple*/
	d3.selectAll("g.group").selectAll(".tickLabels")
		.transition().delay(700).duration(2000)
		.attr("opacity", function(d, i, j) {return j ? 0 : 1; });

	/*Show the Apple name*/
	d3.selectAll(".titles")
	  .transition().duration(2000)
	  .attr("opacity", function(d, i) {return d.index ? 0 : 1; });
	  
	/*Switch  text*/
	changeTopText(newText = "Let us suppose that Lebanon hosts 19% of the world's refugees.",
	loc = 1/2, delayDisappear = 0, delayAppear = 1, finalText = true);
	
	changeBottomText(newText = "",
	loc = 0/2, delayDisappear = 0, delayAppear = 1)	;
	
};/*Draw2*/

/*///////////////////////////////////////////////////////////  
//Draw the other arcs as well
//////////////////////////////////////////////////////////*/
function Draw3(){

	/*First disable click event on clicker button*/
	stopClicker();

	var arcDelay = [0,1,2,12,13,23,33,34,35,40,47];
	/*Show and run the progressBar*/
	runProgressBar(time=700*(arcDelay[(arcDelay.length-1)]+1));	
		
   /*Fill in the other arcs*/
   svg.selectAll("g.group").select("path")
	.transition().delay(function(d, i) { return 700*arcDelay[i];}).duration(1000)
	.style("opacity", op1)
	.attrTween("d", function(d) {
		if(d.index != 0) {
		   var i = d3.interpolate(d.startAngle, d.endAngle);
		   return function(t) {
			   d.endAngle = i(t);
			 return arc(d);
		   }
		}
    });
 
  /*Make the other strokes black as well*/
  svg.selectAll("g.group")
	.transition().delay(function(d,i) { return 700*arcDelay[i]; }).duration(700)
	.selectAll("g").selectAll("line").style("stroke", color1);
  /*Same for the %'s*/
  svg.selectAll("g.group")
	.transition().delay(function(d,i) { return 700*arcDelay[i]; }).duration(700)
	.selectAll("g").selectAll("text").style("opacity", 1);
  /*And the Names of each Arc*/	
  svg.selectAll("g.group")
	.transition().delay(function(d,i) { return 700*arcDelay[i]; }).duration(700)
	.selectAll("text").style("opacity", 1);

	/*Change the text of the top section inside the circle accordingly*/
	/*HTC*/
	changeTopText(newText = "Let us further assume that Jordan hosts 5%, and Germany around 2%.",
		loc = 8/2, delayDisappear = 0, delayAppear = arcDelay[2]);
	/*LG*/
	changeTopText(newText = "All data in this tutorial is hypothetical...",
		loc = 8/2, delayDisappear = arcDelay[3], delayAppear = arcDelay[4]);
	/*Samsung*/
	changeTopText(newText = "These vary from year to year, as people move across borders or are granted asylum/citizenship.",
		loc = 3/2, delayDisappear = (arcDelay[5]-1), delayAppear = arcDelay[5]);
	/*Sony*/
	changeTopText(newText = "...unless",
		loc = 4/2, delayDisappear = arcDelay[6], delayAppear = (arcDelay[8]-1));		
	/*100%*/
	changeTopText(newText = "Together the country shares sum up to 100%.",
		loc = 1/2, delayDisappear = (arcDelay[9]-1), delayAppear = arcDelay[9]);		
	/*Chord intro*/
	changeTopText(newText = "This circle shows how the refugees are currently divided between the countries.",
		loc = 9/2, delayDisappear = (arcDelay[10]-1), delayAppear = arcDelay[10], finalText = true);					
	
	/*Change the text of the bottom section inside the circle accordingly*/
	/*Huawei*/
	changeBottomText(newText = "This means a few hundred thousand people...",
		loc = 4/2, delayDisappear = 0, delayAppear = arcDelay[2]);
	/*Nokia*/
	changeBottomText(newText = "...but we are referring to actual numbers of registered refugees, as per the UNHCR.",
		loc = 1/2, delayDisappear = arcDelay[3], delayAppear = arcDelay[4]);	
	/*Other*/
	changeBottomText(newText = "some countries prefer not to do so and/or send them back home.",
		loc = -1/2, delayDisappear = (arcDelay[5]-1), delayAppear = (arcDelay[8]-1));	
	/*Chord intro*/
	changeBottomText(newText = "Now we did a target-based accounting. The same breakdown can be done for the source countries.",
		loc = 2/2, delayDisappear = (arcDelay[9]-1), delayAppear = arcDelay[10]);	

};/*Draw3*/

/*///////////////////////////////////////////////////////////
//Show the chord between Samsung and Nokia
//////////////////////////////////////////////////////////*/
function Draw4(){

	/*First disable click event on clicker button*/
	stopClicker();
	/*Show and run the progressBar*/
	runProgressBar(time=700*2);	
	
	/*Samsung and Nokia intro text*/
	changeTopText(newText = "First, let us only look at the refugees that are now in Iran, coming from Iraq. Remember, now all numbers are hypothetical.",
		loc = 4, delayDisappear = 0, delayAppear = 1, finalText = true);
		
	/*Bottom text disappear*/
	changeBottomText(newText = "",
		loc = 0, delayDisappear = 0, delayAppear = 1);	
	
    /*Make the non Samsung & Nokia arcs less visible*/
    svg.selectAll("g.group").select("path")
		.transition().duration(1000)
		.style("opacity", function(d) {
			if(d.index != 4 && d.index != 5) {return opacityValue;}
		});		
	
	/*Make the other strokes less visible*/
	d3.selectAll("g.group").selectAll("line")
		.transition().duration(700)
		.style("stroke",function(d,i,j) {if (j == 5 || j == 4) {return color1;} else {return color2;}});
	/*Same for the %'s*/
	svg.selectAll("g.group")
		.transition().duration(700)
		.selectAll(".tickLabels").style("opacity",function(d,i,j) {if (j == 5 || j == 4) {return 1;} else {return opacityValue;}});
	/*And the Names of each Arc*/	
	svg.selectAll("g.group")
		.transition().duration(700)
		.selectAll(".titles").style("opacity", function(d) { if(d.index == 4 || d.index == 5) {return 1;} else {return opacityValue;}});

	/*Show only the Samsung Nokia chord*/
	chords.transition().duration(2000)
		.attr("opacity", function(d, i) { 
			if(d.source.index == 5 && d.target.index == 4) 
				{return opacityValueBase;}
			else {return 0;}
		});
	
};/*Draw4*/

/*//////////////////////////////////////////////////////////////////////////*/
function Draw5(){

	/*First disable click event on clicker button*/
	stopClicker();
	/*Show and run the progressBar*/
	runProgressBar(time=700*2);	
	
	/*Samsung and Nokia text*/
	changeTopText(newText = "On the left, touching the arc of Iran, we can see that the chord runs from 17% to almost 26%. Which is a thickness spanning 9%.",
		loc = 4, delayDisappear = 0, delayAppear = 1, finalText = true);
	
    /*Make the non Samsung & Nokia arcs less visible*/
    svg.selectAll("g.group").select("path")
		.transition().duration(1000)
		.style("opacity", opacityValue);		

	/*Show only the Samsung Nokia part at Samsung*/
	var arcSamsung = d3.svg.arc()
				.innerRadius(innerRadius)
				.outerRadius(outerRadius)
				.startAngle(4.040082626337902)
				.endAngle(4.561777856121815);
				
	svg.append("path")
		.attr("class","SamsungToNokiaArc")
		.attr("d", arcSamsung)
		.attr("fill", colors[5])
		.style('stroke', colors[5]);
		
	repeat();
	
	/*Repeatedly let an arc change colour*/
	function repeat() {
		d3.selectAll(".SamsungToNokiaArc")
			.transition().duration(700)
			.attr("fill", colors[5])
			.style('stroke', colors[5])
			.transition().duration(700)
			.attr("fill", colors[5])
			.style('stroke', colors[5])
			.each("end", repeat)
			;
	};
	
};/*Draw5*/

/*//////////////////////////////////////////////////////////////////////////*/
function Draw6(){

	/*First disable click event on clicker button*/
	stopClicker();
	/*Show and run the progressBar*/
	runProgressBar(time=700*2);	
	
	/*Samsung and Nokia text*/
	changeTopText(newText = "These 9% of the refugees now are in Iran and by following the chord we can see where are they coming from, which in this case, is Iraq.",
		loc = 4, delayDisappear = 0, delayAppear = 1, finalText = true);

	/*Show only the Samsung Nokia part at Nokia*/
	var arcNokia = d3.svg.arc()
				.innerRadius(innerRadius)
				.outerRadius(outerRadius)
				.startAngle(2.837816067671451)
				.endAngle(2.9104595910835127);

	svg.append("path")
		.attr("class","NokiaToSamsungArc")
		.attr("d", arcNokia)
		.attr("opacity", 0)
		.attr("fill", colors[4])
		.transition().duration(700)
		.attr("opacity", 1)
		.attr("stroke", colors[4]);				
		
};/*Draw6*/

/*//////////////////////////////////////////////////////////////////////////*/
function Draw7(){

	/*First disable click event on clicker button*/
	stopClicker();
	/*Show and run the progressBar*/
	runProgressBar(time=700*11);	
	
	/*Samsung and Nokia text*/
	changeTopText(newText = "At the Iraq side, the arc is much thinner, only spanning 1.2% (of all refugees)",
		loc = 4, delayDisappear = 0, delayAppear = 1);
	changeTopText(newText = "These 1.2% are now in Iraq, but by following the chord we can see that they come from Iran.",
		loc = 4, delayDisappear = 9, delayAppear = 10, finalText = true);
		
	/*Stop the color changing on the Samsung side*/
	d3.selectAll(".SamsungToNokiaArc")
		.transition().duration(700)
		.attr("fill", colors[5])
		.style("stroke", colors[5]);

	/*Repeatedly let an arc change colour*/		
	repeat();
	function repeat() {
		d3.selectAll(".NokiaToSamsungArc")
			.transition().duration(700)
			.attr("fill", color1)
			.style('stroke', color2)
			.transition().duration(700)
			.attr("fill", colors[5])
			.style("stroke", colors[5])
			.each("end", repeat)
			;
	};
				
};/*Draw7*/

/*//////////////////////////////////////////////////////////////////////////*/
function Draw8(){

	/*First disable click event on clicker button*/
	stopClicker();
	/*Show and run the progressBar*/
	runProgressBar(time=700*11);	
	
	/*Samsung and Nokia text*/
	changeTopText(newText = "Since the chord is much wider at the Iran side, Iran has taken a lot more refugees from Iraq than Iran sent to Iraq.",
		loc = 4, delayDisappear = 0, delayAppear = 1);
	changeTopText(newText = "Therefore, the chord is the color of Iran's blue, since Iran has the net gain from the exchange of people between Iran and Iraq.",
		loc = 4, delayDisappear = 9, delayAppear = 10, finalText = true);
		
	/*Stop the colour changing on the Nokia side*/
	d3.selectAll(".NokiaToSamsungArc")
		.transition().duration(700)
		.attr("fill", colors[5])
		.style("stroke", colors[5]);
				
};/*Draw8*/

/*///////////////////////////////////////////////////////////	
//Show Loyalty hills
//////////////////////////////////////////////////////////*/
function Draw9(){

	/*First disable click event on clicker button*/
	stopClicker();
	/*Show and run the progressBar*/
	runProgressBar(time=700*20);	
	
	/*Samsung Loyal text*/
	changeTopText(newText = "In some cases the source and target country are the same. These are internally displaced persons (IDPs).",
		loc = 4/2, delayDisappear = 0, delayAppear = 1, finalText = false, xloc=-50, w=300);
	changeTopText(newText = "These refugees are represented by the hills at each country.",
		loc = 3/2, delayDisappear = 9, delayAppear = 10, finalText = false, xloc=-50, w=300);
	changeTopText(newText = "You can also envision this as a chord beginning and ending on itself.",
		loc = 2/2, delayDisappear = 18, delayAppear = 19, finalText = true, xloc=-50, w=300);
		
	/*Remove the arcs*/
	d3.selectAll(".NokiaToSamsungArc")
		.transition().duration(2000)
		.attr("opacity", 0)
		.each("end", function() {d3.selectAll(".NokiaToSamsungArc").remove();});

	d3.selectAll(".SamsungToNokiaArc")
		.transition().duration(2000)
		.attr("opacity", 0)
		.each("end", function() {d3.selectAll(".SamsungToNokiaArc").remove();});
		
	/*Show only the loyal chords*/
	chords.transition().duration(2000)
		.attr("opacity", function(d, i) { 
			if(d.source.index == 0 && d.target.index == 0) {return opacityValueBase;}
			else if(d.source.index == 1 && d.target.index == 1) {return opacityValueBase;}
			else if(d.source.index == 2 && d.target.index == 2) {return opacityValueBase;}
			else if(d.source.index == 3 && d.target.index == 3) {return opacityValueBase;}
			else if(d.source.index == 4 && d.target.index == 4) {return opacityValueBase;}
			else if(d.source.index == 5 && d.target.index == 5) {return opacityValueBase;}
			else if(d.source.index == 6 && d.target.index == 6) {return opacityValueBase;}
			else if(d.source.index == 7 && d.target.index == 7) {return opacityValueBase;}
			else {return 0;}
		});
	
		
	/*Show all ticks and texts again*/
	/*Ticks*/
	d3.selectAll("g.group").selectAll("line")
		.transition().duration(700)
		.style("stroke", color1);
	/*Same for the %'s*/
	svg.selectAll("g.group")
		.transition().duration(700)
		.selectAll(".tickLabels").style("opacity", 1);
	/*And the Names of each Arc*/	
	svg.selectAll("g.group")
		.transition().duration(700)
		.selectAll(".titles").style("opacity", 1);
				
};/*Draw9*/

/*//////////////////////////////////////////////////////////////////////////*/
function Draw10(){

	/*First disable click event on clicker button*/
	stopClicker();
	/*Show and run the progressBar*/
	runProgressBar(time=700*11);
	
	changeTopText(newText = "This can be true for groups of countries,",
		loc = 6/2, delayDisappear = 0, delayAppear = 1);
		changeTopText(newText = "when many smaller country flows are aggregated into one.",
		loc = 6/2, delayDisappear = 9, delayAppear = 10, finalText = true);
		
	/*Show only the Nokia Loyal arc*/
	var arcNokia = d3.svg.arc()
				.innerRadius(innerRadius)
				.outerRadius(outerRadius)
				.startAngle(2.048671976860533)
				.endAngle(2.6694216777820063);

	svg.append("path")
		.attr("class","NokiaLoyalArc")
		.attr("d", arcNokia)
		.attr("opacity", 1)
		.attr("stroke", colors[4])
		.attr("fill", colors[4]);	

	/*Repeatedly let an arc change colour*/		
	repeat();
	
	function repeat() {
		d3.selectAll(".NokiaLoyalArc")
			.transition().duration(700)
			.attr("fill", color1)
			.style('stroke', color2)
			.transition().duration(700)
			.attr("fill", colors[4])
			.style("stroke", colors[4])
			.each("end", repeat);
	};
	
	/*Show only the Nokia loyal chord*/
	chords.transition().duration(2000)
		.attr("opacity", function(d, i) { 
			if(d.source.index == 4 && d.target.index == 4) {return opacityValueBase;}
			else {return 0;}
		});		

	/*Make the other strokes less visible*/
	d3.selectAll("g.group").selectAll("line")
		.transition().duration(700)
		.style("stroke",function(d,i,j) {if (j == 4) {return color1;} else {return color2;}});
	/*Same for the %'s*/
	svg.selectAll("g.group")
		.transition().duration(700)
		.selectAll(".tickLabels").style("opacity",function(d,i,j) {if (j == 4) {return 1;} else {return opacityValue;}});
	/*And the Names of each Arc*/	
	svg.selectAll("g.group")
		.transition().duration(700)
		.selectAll(".titles").style("opacity", function(d) { if(d.index == 4) {return 1;} else {return opacityValue;}});

};/*Draw10*/

/*//////////////////////////////////////////////////////////
//Show all chords that are connected to Apple
//////////////////////////////////////////////////////////*/
function Draw11(){

	/*First disable click event on clicker button*/
	stopClicker();
	/*Show and run the progressBar*/
	runProgressBar(time=700*2);	
	
	changeTopText(newText = "Here are all the people finding refuge in Lebanon.",
		loc = 3/2, delayDisappear = 0, delayAppear = 1, finalText = true, xloc=-80, w=200);
		
	/*Remove the Nokia arc*/
	d3.selectAll(".NokiaLoyalArc")
		.transition().duration(1000)
		.attr("opacity", 0)
		.each("end", function() {d3.selectAll(".NokiaLoyalArc").remove();});
			
	/*Only show the chords of Apple*/
	chords.transition().duration(2000)
    .attr("opacity", function(d, i) { 
		if(d.source.index == 0 || d.target.index == 0) {return opacityValueBase;}
		else {return 0;}
	});

	/*Highlight arc of Apple*/
	svg.selectAll("g.group").select("path")
		.transition().duration(2000)
		.style("opacity", function(d) {
			if(d.index != 0) {return opacityValue;}
		});	
		
	/*Show only the ticks and text at Apple*/
	/*Make the other strokes less visible*/
	d3.selectAll("g.group").selectAll("line")
		.transition().duration(700)
		.style("stroke",function(d,i,j) {if (j == 0) {return color1;} else {return color2;}});
	/*Same for the %'s*/
	svg.selectAll("g.group")
		.transition().duration(700)
		.selectAll(".tickLabels").style("opacity",function(d,i,j) {if (j == 0) {return 1;} else {return opacityValue;}});
	/*And the Names of each Arc*/	
	svg.selectAll("g.group")
		.transition().duration(700)
		.selectAll(".titles").style("opacity", function(d) { if(d.index == 0) {return 1;} else {return opacityValue;}});

};/*Draw11*/

function Draw12(){

	/*First disable click event on clicker button*/
	stopClicker();
	/*Show and run the progressBar*/
	runProgressBar(time=700*11);	

	changeTopText(newText = "One thing that stands out for Lebanon is that all chords connected to " +
							"it have it's color: pink.",
		loc = 3/2, delayDisappear = 0, delayAppear = 1, finalText = false, xloc=-80, w=210);
	changeTopText(newText = "This means that Lebanon has always had the net gain. " + 
							"They received more refugees from other countries than they sent to them.",
		loc = 4/2, delayDisappear = 9, delayAppear = 10, finalText = true, xloc=-80, w=210);

};/*Draw12*/
  
  
function Draw13(){

	/*First disable click event on clicker button*/
	stopClicker();
	/*Show and run the progressBar*/
	runProgressBar(time=700*11);	

	changeTopText(newText = "Even more so, apart from the chord to Iran, all other chords are extremely narrow at the other end from Lebanon.",
		loc = 3/2, delayDisappear = 0, delayAppear = 1, finalText = false, xloc=-80, w=200);
	changeTopText(newText = "This means that Lebanon is a relatively well-established asylum.",
		loc = 3/2, delayDisappear = 9, delayAppear = 10, finalText = true, xloc=-80, w=200);	
	
	/*Repeatedly let specific chords change colour*/
	repeat();
	
	function repeat() {
		chords
			.transition().duration(1000)
			.style("opacity",function (d){
				if(d.source.index == 0) {
					if(d.target.index == 0 || d.target.index == 5) {return opacityValueBase;}
					else {return 0.2;}
				} else {return 0;}
			})
			.transition().duration(1000)
			.style("opacity",function (d){
				if(d.source.index == 0) {return opacityValueBase;}
				else {return 0;}
			})
			.each("end", repeat);
	};	
};/*Draw13*/


function Draw14(){

	/*First disable click event on clicker button*/
	stopClicker();
	/*Show and run the progressBar*/
	/*runProgressBar(time=700*2);*/

	changeTopText(newText = "Thank you for staying with me so far! After these examples I think you're absolutely " + 
							"ready to face the full impact of all chords simultaneously!",
		loc = 9/2, delayDisappear = 0, delayAppear = 1, finalText = true);
		
	changeBottomText(newText = "I'm looking forward to hearing about the insights that you have discovered on your own!",
		loc = 5/2, delayDisappear = 0, delayAppear = 1);		
	
	/*Only show the chords of Apple*/
	chords.transition().duration(1000)
		.style("opacity", 0.1);

	/*Hide all the text*/
	d3.selectAll("g.group").selectAll("line")
		.transition().duration(700)
		.style("stroke",bgcolor);
	/*Same for the %'s*/
	svg.selectAll("g.group")
		.transition().duration(700)
		.selectAll(".tickLabels").style("opacity",0.4);
	/*And the Names of each Arc*/	
	svg.selectAll("g.group")
		.transition().duration(700)
		.selectAll(".titles").style("opacity",0.4);	
		
};/*Draw14*/

function Draw15(){

	/*First disable click event on clicker button*/
	stopClicker();
	/*Show and run the progressBar*/
	/*runProgressBar(time=700*2);*/

	changeTopText(newText = "Now you will enter the main app. It has two chord diagrams, side-by-side. You already know how to read them!",
		loc = 10/2, delayDisappear = 0, delayAppear = 1, finalText = true);
		
	changeBottomText(newText = "One of them is a target-based, while the other one is a source-based accounting. This means they display the receiving or the sending countries.",
		loc = 3/2, delayDisappear = 0, delayAppear = 1);		
	
	/*Only show the chords of Apple*/
	chords.transition().duration(1000)
		.style("opacity", 0.1);

	/*Hide all the text*/
	d3.selectAll("g.group").selectAll("line")
		.transition().duration(700)
		.style("stroke",bgcolor);
	/*Same for the %'s*/
	svg.selectAll("g.group")
		.transition().duration(700)
		.selectAll(".tickLabels").style("opacity",0.4);
	/*And the Names of each Arc*/	
	svg.selectAll("g.group")
		.transition().duration(700)
		.selectAll(".titles").style("opacity",0.4);	
		
};/*Draw15*/

function Draw16(){

	/*First disable click event on clicker button*/
	stopClicker();
	/*Show and run the progressBar*/
	/*runProgressBar(time=700*2);*/

	changeTopText(newText = "You can filter out some countries from the diagram by clicking on their label.",
		loc = 9/2, delayDisappear = 0, delayAppear = 1, finalText = true);
		
	changeBottomText(newText = "And you can also filter out all countries with flows smaller than a threshold (set to 100 000 people by default).",
		loc = 1/2, delayDisappear = 0, delayAppear = 1);		
	
	/*Only show the chords of Apple*/
	chords.transition().duration(1000)
		.style("opacity", 0.1);

	/*Hide all the text*/
	d3.selectAll("g.group").selectAll("line")
		.transition().duration(700)
		.style("stroke",bgcolor);
	/*Same for the %'s*/
	svg.selectAll("g.group")
		.transition().duration(700)
		.selectAll(".tickLabels").style("opacity",0.4);
	/*And the Names of each Arc*/	
	svg.selectAll("g.group")
		.transition().duration(700)
		.selectAll(".titles").style("opacity",0.4);	
		
};/*Draw16*/

function Draw17(){

	/*First disable click event on clicker button*/
	stopClicker();
	/*Show and run the progressBar*/
	/*runProgressBar(time=700*2);*/

	changeTopText(newText = "Remember, all data is dynamic! Drag the time slider, scroll with your mouse or use the arrow keys to change the year.",
		loc = 6/2, delayDisappear = 0, delayAppear = 1, finalText = true);
		
	changeBottomText(newText = "Play! Enjoy! Share!",
		loc = 7/2, delayDisappear = 0, delayAppear = 1);		
	
	/*Only show the chords of Apple*/
	chords.transition().duration(1000)
		.style("opacity", 0.1);

	/*Hide all the text*/
	d3.selectAll("g.group").selectAll("line")
		.transition().duration(700)
		.style("stroke",bgcolor);
	/*Same for the %'s*/
	svg.selectAll("g.group")
		.transition().duration(700)
		.selectAll(".tickLabels").style("opacity",0.4);
	/*And the Names of each Arc*/	
	svg.selectAll("g.group")
		.transition().duration(700)
		.selectAll(".titles").style("opacity",0.4);	
		
};/*Draw17*/

/*///////////////////////////////////////////////////////////
//Draw the original Chord diagram
///////////////////////////////////////////////////////////*/
/*Go to the final bit*/

function finalChord() {
	
	window.parent.document.getElementById('content').src="parent.html";

};/*finalChord*/

/*//////////////////////////////////////////////////////////
////////////////// Extra Functions /////////////////////////
//////////////////////////////////////////////////////////*/

/*Returns an event handler for fading a given chord group*/
function fade(opacity) {
  return function(d, i) {
    svg.selectAll("path.chord")
        .filter(function(d) { return d.source.index != i && d.target.index != i; })
		.transition()
        .style("stroke-opacity", opacity)
        .style("fill-opacity", opacity);
  };
};/*fade*/

/*Returns an array of tick angles and labels, given a group*/
function groupTicks(d) {
  var k = (d.endAngle - d.startAngle) / d.value;
  return d3.range(0, d.value, 1).map(function(v, i) {
    return {
      angle: v * k + d.startAngle,
      label: i % 5 ? null : v + "%"
    };
  });
};/*groupTicks*/

/*Taken from https://groups.google.com/forum/#!msg/d3-js/WC_7Xi6VV50/j1HK0vIWI-EJ
//Calls a function only after the total transition ends*/
function endall(transition, callback) { 
    var n = 0; 
    transition 
        .each(function() { ++n; }) 
        .each("end", function() { if (!--n) callback.apply(this, arguments); }); 
};/*endall*/ 

/*Taken from http://bl.ocks.org/mbostock/7555321
//Wraps SVG text*/
function wrap(text, width) {
    var text = d3.select(this)[0][0],
        words = text.text().split(/\s+/).reverse(),
        word,
        line = [],
        lineNumber = 0,
        lineHeight = 1.4, 
        y = text.attr("y"),
		x = text.attr("x"),
        dy = parseFloat(text.attr("dy")),
        tspan = text.text(null).append("tspan").attr("x", x).attr("y", y).attr("dy", dy + "em");
		
    while (word = words.pop()) {
      line.push(word);
      tspan.text(line.join(" "));
      if (tspan.node().getComputedTextLength() > width) {
        line.pop();
        tspan.text(line.join(" "));
        line = [word];
        tspan = text.append("tspan").attr("x", x).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
      };
    };  
};

/*Transition the top circle text*/
function changeTopText (newText, loc, delayDisappear, delayAppear, finalText, xloc, w) {

	/*If finalText is not provided, it is not the last text of the Draw step*/
	if(typeof(finalText)==='undefined') finalText = false;
	
	if(typeof(xloc)==='undefined') xloc = 0;
	if(typeof(w)==='undefined') w = 350;
	
	middleTextTop	
		/*Current text disappear*/
		.transition().delay(700 * delayDisappear).duration(700)
		.attr('opacity', 0)	
		/*New text appear*/
		.call(endall,  function() {
			middleTextTop.text(newText)
			.attr("y", -24*loc + "px")
			.attr("x", xloc + "px")
			.call(wrap, w);	
		})
		.transition().delay(700 * delayAppear).duration(700)
		.attr('opacity', 1)
		.call(endall,  function() {
			if (finalText == true) {
				d3.select("#clicker")
					.text(buttonTexts[counter-2])
					.style("pointer-events", "auto")
					.transition().duration(400)
					.style("border-color", color1)
					.style("color", color1);
				};
		});
};/*changeTopText */

/*Transition the bottom circle text*/
function changeBottomText (newText, loc, delayDisappear, delayAppear) {
	middleTextBottom
		/*Current text disappear*/
		.transition().delay(700 * delayDisappear).duration(700)
		.attr('opacity', 0)
		/*New text appear*/
		.call(endall,  function() {
			middleTextBottom.text(newText)
			.attr("y", 24*loc + "px")
			.call(wrap, 350);	
		})
		.transition().delay(700 * delayAppear).duration(700)
		.attr('opacity', 1);
;}/*changeTopText*/

/*Stop clicker from working*/
function stopClicker() {
	d3.select("#clicker")
		.style("pointer-events", "none")
		.transition().duration(400)
		.style("border-color", color2)
		.style("color", color2);
};/*stopClicker*/

/*Run the progress bar during an animation*/
function runProgressBar(time) {	
	
	/*Make the progress div visible*/
	d3.selectAll("#progress")
		.style("visibility", "visible");
	
	/*Linearly increase the width of the bar
	//After it is done, hide div again*/
	d3.selectAll(".prgsFront")
		.transition().duration(time).ease("linear")
		.attr("width", prgsWidth)
		.call(endall,  function() {
			d3.selectAll("#progress")
				.style("visibility", "hidden");
		});
	
	/*Reset to zero width*/
	d3.selectAll(".prgsFront")
		.attr("width", 0);
		
};/*runProgressBar*/